from django.shortcuts import render
from .models import *
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
# Create your views here.

def get_flight_data(queryset):
    data = []
    for flight in queryset:
        data_small = {
            "id":flight.id,
            "name":flight.name,
            "source":flight.source,
            "destination":flight.destination,
            "start_time":flight.start_time,
        }
        data.append(data_small)
    return data

def get_seat_data(queryset, request=None):
    data = []
    for seat in queryset:
        data_small = {
            "id":seat.id,
            "name":seat.name,
            "is_booked":Booking.objects.filter(seat=seat).exclude(status="Completed").exclude(status="Cancelled").exists(),
        }
        if request:
            data_small["booked_by_you"] = Booking.objects.filter(seat=seat, user=request.user).exclude(status="Completed").exclude(status="Cancelled").exists()
        data.append(data_small)
    return data

def get_booking_data(queryset):
    data = []
    for booking in queryset:
        data_small = {
            "id":booking.id,
            "seat":booking.seat.name,
            "status":booking.status,
            "created_at":booking.created_at,
            "seat_id":booking.seat.id,
        }
        data.append(data_small)
    return data

def get_single_booking_data(booking):
    data = {
        "id":booking.id,
        "seat":booking.seat.name,
        "status":booking.status,
        "created_at":booking.created_at,
        "seat_id":booking.seat.id,
    }
    return data


def FlightListView(request):
    if(request.method.lower() == "post"):
        current_user = authenticate(email=request.POST.get("name"), password=request.POST.get("password"))
        print(request.user)
    flights = Flight.objects.all()
    return render(request, "flightlist.html", context={"data":flights})


def GetSeatListView(request):
    if not request.user:
        return redirect("login")
    already=False
    if request.method=="POST":
        seat = Seat.objects.get(id=request.POST.get('seat_id'))
        if Booking.objects.filter(seat=seat).exclude(status="Completed").exclude(status="Cancelled").exists():
            already=True
        else:
            booking = Booking.objects.create(seat=seat, user=request.user, status="Pending")
        flight = Flight.objects.get(id=request.POST.get('flight_id'))
    else:
        flight = Flight.objects.get(id=request.GET.get('flight_id'))
    
    seats = Seat.objects.filter(flight=flight)
    return render(request, "seatlist.html", context={"data":get_seat_data(seats, request), "flight_id":flight.id, "already":already, "booking_id":0})


def BookSeatView(request):
    if not request.user:
        return redirect("login")
    already=False
    if request.method=="POST":
        seat = Seat.objects.get(id=request.POST.get('seat_id'))
        if Booking.objects.filter(seat=seat).exclude(status="Completed").exclude(status="Cancelled").exists():
            already=True
            booking = Booking.objects.get(seat=seat)
        booking = Booking.objects.create(seat=seat, user=request.user, status="Pending")
    else:
        seat = Seat.objects.get(id=request.GET.get('seat_id'))
    user = request.user
    return render(request, "booked.html", context={"data":booking.id, "already":already})


def BookingListView(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, "bookinglist.html", context={"data":get_booking_data(bookings)})

def CancelBookingView(request):
    booking = Booking.objects.get(id=request.GET.get('booking_id'))
    booking.status = "Cancelled"
    booking.save()
    return render(request, "cancelled.html")

# def GetBookingView(request):
#     booking = Booking.objects.get(id=request.GET.get('booking_id'))
#     return render(request, "booking.html", context={"data":get_booking_data([booking])})

def GetBookingView(request):
    if not request.user:
        return redirect("login")
    if request.method=="POST" and request.POST.get('status') == "confirm":
        print(request.POST)
        booking = Booking.objects.get(seat_id=int(request.POST.get('seat_id')), user=request.user)
        booking.status = "Confirmed"
        booking.save()
    elif request.method=="POST" and request.POST.get('status') == "cancel":
        print(request.POST)
        booking = Booking.objects.get(seat_id=int(request.POST.get('seat_id')), user=request.user)
        booking.status = "Cancelled"
        booking.save()
        cancellation = Cancellation.objects.create(booking=booking, reason=request.POST.get('cancel_reason'))
    else:
        booking = Booking.objects.get(seat_id=int(request.GET.get('seat_id')), user=request.user)
    return render(request, "booking.html", context={"booking":get_single_booking_data(booking)})