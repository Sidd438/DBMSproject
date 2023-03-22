from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
# Create your views here.
def login(request):
    return render(request, "login.html")