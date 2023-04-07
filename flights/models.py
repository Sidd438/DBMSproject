from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    use_in_migrations = True
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        if not password:
            raise ValueError('Users must have an password address')

        email = self.normalize_email(email)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user


    def create_superuser(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user




class Passenger(AbstractUser):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('NB','Non-Binary')
    )
    username=None
    password = models.CharField(max_length=100)
    email = models.EmailField(_('email address'), primary_key=True)
    date_of_birth = models.DateField(blank=True,null=True)
    gender = models.CharField(_('gender'),max_length=2, choices=GENDER_CHOICES)
    name = models.CharField(max_length=100)
    expense = models.IntegerField(default=0)
    is_superuser = models.BooleanField(_('superuser status'),default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    class Meta:
        db_table = "passengers"
# Create your models here.
BOOKING_STATUS_CHOICES = [
    ("Pending", "Pending"),
    ("Confirmed", "Confirmed"), 
    ("Cancelled", "Cancelled"),
    ("Completed", "Completed")
]
from django.contrib.auth import get_user_model
UserC = get_user_model()

class Flight(models.Model):
    name = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    price = models.IntegerField()
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)


    def __str__(self) -> str:
        return self.name +" " + self.source + "---" + self.destination
    
    class Meta:
        unique_together = ["start_time", "end_time", "source", "destination"]
        db_table = "flights"
    


class Seat(models.Model):
    id=None
    name = models.CharField(max_length=100)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name="seats")

    class Meta:
        unique_together = ["name", "flight"]
        db_table = "seats"



class Booking(models.Model):
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE, related_name="bookings")
    status = models.CharField(max_length=20, choices=BOOKING_STATUS_CHOICES)
    user = models.ForeignKey(UserC, related_name="Bookings", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # unique_together = ["seat", "user"]
        db_table = "bookings"



class Cancellation(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name="cancellation", primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    reason = models.TextField()

    class Meta:
        db_table = "cancellations"


class Email(models.Model):
    recepient = models.ForeignKey(UserC, on_delete=models.CASCADE, related_name="emails")
    subject = models.CharField(max_length=100)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "emails"


class SMS(models.Model):
    recepient = models.ForeignKey(UserC, on_delete=models.CASCADE, related_name="sms")
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "sms"