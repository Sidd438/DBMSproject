from django.shortcuts import render
from .models import *
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.db import connection
import mysql.connector
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
            "end_time":flight.end_time,
            "price":flight.price,
        }
        data.append(data_small)
    return data

def get_seat_data(queryset, request=None):
    data = []
    for seat in queryset:
        data_small = {
            "id":seat.id,
            "name":seat.name,
            "is_booked":False,
        }
        booking = Booking.objects.raw("SELECT * FROM bookings WHERE bookings.seat_id = %s AND bookings.status != 'Completed' AND bookings.status != 'Cancelled'", [seat.id])
        if booking:
            data_small["is_booked"] = True
        if request:
            booking = Booking.objects.raw("SELECT * FROM bookings WHERE bookings.seat_id = %s AND bookings.status != 'Completed' AND bookings.status != 'Cancelled' AND bookings.user_id = %s", [seat.id, request.user.id])
            if booking:
                data_small["booking_id"] = booking[0].id
                data_small["status"] = booking[0].status
                data_small["booked_by_you"] = True
            else:
                data_small["booked_by_you"] = False

        data.append(data_small)
    return data

def get_booking_data(queryset):
    data = []
    for booking in queryset:
        seat = Seat.objects.raw(f'SELECT * FROM seats WHERE seats.id = {booking.seat.id}')[0]
        data_small = {
            "id":booking.id,
            "seat":seat.name,
            "status":booking.status,
            "created_at":booking.created_at,
            "seat_id":seat.id,
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
        query = f'SELECT * FROM passengers WHERE (passengers.email = "{request.POST.get("name")}" AND passengers.password =  {request.POST.get("password")})'
        print(query)
        # current_user = UserC.objects.filter(email=request.POST.get("name"), password=request.POST.get("password")).first()
        current_user = UserC.objects.raw(f'SELECT * FROM passengers WHERE (passengers.email = "{request.POST.get("name")}" AND passengers.password =  "{request.POST.get("password")}")')[0]
        if not current_user:
            return redirect("login")
        login(request, current_user)
        # request.user = current_user
    query = f"select * from flights where 1=1"
    print(request.method)
    if request.method == "GET":
        if request.GET.get('destination'):
            query += f" and destination = '{request.GET.get('destination')}'"
        if request.GET.get('source'):
            query += f" and source = '{request.GET.get('source')}'"
    flights = Flight.objects.raw(query)
    return render(request, "flightlist.html", context={"data":flights, "destination":request.GET.get('destination'), "source":request.GET.get('source')})


def SearchFlightView(request):
    if not request.user:
        return redirect("login")
    return render(request, "searchbox.html", context={"destination":request.POST.get('destination'), "source":request.POST.get('source')})


def GetSeatListView(request):
    if not request.user:
        return redirect("login")
    already=False
    print(request.user, request.method)
    if request.method=="POST":
        seat = Seat.objects.raw(f"select * from seats where id = {request.POST.get('seat_id')}")[0]
        bookings = Booking.objects.raw(f"select * from bookings where seat_id = {seat.id} and user_id = {request.user.id} and (status = 'Pending' or status='Confirmed')")
        print(len(bookings))
        if len(bookings):
            already=True
        else:
            cursor = connection.cursor()
            cursor.execute(f"insert into bookings (seat_id, user_id, status, created_at) values ({seat.id}, {request.user.id}, 'Pending', NOW())")
            # Booking.objects.raw(f"insert into booking (seat_id, user_id, status, created_at) values ({seat.id}, {request.user.id}, 'Pending', NOW())")
        flight = Flight.objects.raw(f"select * from flights where id = {request.POST.get('flight_id')}")[0]
    else:
        flight = Flight.objects.raw(f"select * from flights where id = {request.GET.get('flight_id')}")[0]
    seats = Seat.objects.raw(f"select * from seats where flight_id = {flight.id}")
    return render(request, "seatlist.html", context={"data":get_seat_data(seats, request), "flight_id":flight.id, "already":already, "booking_id":0})


# def BookSeatView(request):
#     if not request.user:
#         return redirect("login")
#     already=False
#     if request.method=="POST":
#         seat = Seat.objects.raw(f"select * from seat where id = {request.POST.get('seat_id')}")[0]
#         if Booking.objects.filter(seat=seat).exclude(status="Completed").exclude(status="Cancelled").exists():
#             already=True
#             booking = Booking.objects.get(seat=seat)
#         booking = Booking.objects.create(seat=seat, user=request.user, status="Pending")
#     else:
#         seat = Seat.objects.get(id=request.GET.get('seat_id'))
#     return render(request, "booked.html", context={"data":booking.id, "already":already})


def BookingListView(request):
    bookings = Booking.objects.raw(f"select * from bookings where user_id = {request.user.id}")
    return render(request, "bookinglist.html", context={"data":get_booking_data(bookings)})

def CancelBookingView(request):
    Booking.objects.raw(f"update bookings set status = 'Cancelled' where id = {request.GET.get('booking_id')}")
    return render(request, "cancelled.html")

# def GetBookingView(request):
#     booking = Booking.objects.get(id=request.GET.get('booking_id'))
#     return render(request, "booking.html", context={"data":get_booking_data([booking])})

def GetBookingView(request):
    cursor = connection.cursor()
    if not request.user:
        return redirect("login")
    if request.method=="POST" and request.POST.get('status') == "confirm":
        cursor.execute(f"update bookings set status = 'Confirmed' where id = {request.POST.get('booking_id')}")
        booking = Booking.objects.raw(f"select * from bookings where id = {request.POST.get('booking_id')}")[0]
    elif request.method=="POST" and request.POST.get('status') == "cancel":
        cursor.execute(f"update bookings set status = 'Cancelled' where id = {request.POST.get('booking_id')}")
        cursor.execute(f"insert into cancellations (booking_id, reason, created_at) values ({request.POST.get('booking_id')}, '{request.POST.get('cancel_reason')}', NOW())")
        booking = Booking.objects.raw(f"select * from bookings where id = {request.POST.get('booking_id')}")[0]
    else:
        booking = Booking.objects.raw(f"select * from bookings where id = {request.GET.get('booking_id')}")[0]       
    return render(request, "booking.html", context={"booking":get_single_booking_data(booking)})