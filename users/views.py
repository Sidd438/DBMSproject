from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
# Create your views here.
User = get_user_model()
def login(request):
    logout(request)
    return render(request, "login.html")


def reqistration(request):
    if request.method == "POST":
        email = request.POST["email"]
        name = request.POST["name"]
        password = request.POST["password"]
        dob = request.POST["date"]
        user = User.objects.create(email=email, name=name, password=password, date_of_birth=dob)
        user.save()
        return redirect("login")
    return render(request, "registration.html")