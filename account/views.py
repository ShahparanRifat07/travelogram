from django.shortcuts import render, redirect
from .models import CustomUser, Code, Profile

from django.contrib.auth import authenticate, login, logout


# Create your views here.

def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        phone = request.POST.get("phone")
        password = request.POST.get("password")

        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            user = None

        if user is not None:
            print("username already exits")
            return redirect(signup)
        else:
            new_user = CustomUser(username=username, phone_number=phone)
            new_user.set_password(password)
            new_user.save()
            login(request, new_user)
            return render(request, 'home.html')
    else:
        return render(request, 'signup.html')


def signin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'home.html')

        else:
            return redirect('login')
    else:
        return render(request, 'login.html')
