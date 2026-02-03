from django.shortcuts import render, redirect
from  django.contrib import messages
from  django.contrib.auth import authenticate, login, logout
from .models import User

def home(rquest):
    return redirect("login")

def signup_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        role = request.POST.get("role")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("signup")

        User.objects.create_user(
            username=username,
            password=password,
            email=email,
            roles=role
        )

        messages.success(request, "Account created successfully")
        return redirect("login")

    return render(request, "accounts/signup.html")

def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.error(request, "Invalid username or password")
            return redirect("login")

        login(request, user)
        messages.success(request, "Logged in successfully")

        if user.roles == "recruiter":
            return redirect("recruiter_dashboard")
        elif user.roles == "jobseeker":
            return redirect("jobseeker_dashboard")

        return redirect("login")

    return render(request, "accounts/login.html")


def logout_page(request):
    logout(request)
    messages.warning(request,"You have been Logged Out")
    return redirect("login")
