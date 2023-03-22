from django.db import models
from django.contrib.auth import get_user_model
UserC = get_user_model()
# Create your models here.
BOOKING_STATUS_CHOICES = [
    ("Pending", "Pending"),
    ("Confirmed", "Confirmed"), 
    ("Cancelled", "Cancelled"),
    ("Completed", "Completed")
]

class Flight(models.Model):
    name = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)


    def __str__(self) -> str:
        return self.name +" " + self.source + "---" + self.destination
    


class Seat(models.Model):
    name = models.CharField(max_length=100)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name="seats")



class Booking(models.Model):
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE, related_name="bookings")
    status = models.CharField(max_length=20, choices=BOOKING_STATUS_CHOICES)
    user = models.ForeignKey(UserC, related_name="Bookings", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["seat", "user"]


class Cancellation(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="cancellations")
    created_at = models.DateTimeField(auto_now_add=True)
    reason = models.TextField()