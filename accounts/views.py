from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from applications.models import Application
from jobs.models import Job
from .models import User


def home(request):
    if request.user.is_authenticated:
        if request.user.roles == "jobseeker":
            return redirect("jobseeker_dashboard")
        elif request.user.roles == "recruiter":
            return redirect("recruiter_dashboard")
    return redirect("login")


def signup_page(request):
    if request.user.is_authenticated:
        messages.info(request, "You already have an account.")
        return redirect("profile")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        role = request.POST.get("role")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("signup")

        User.objects.create_user(
            username=username, password=password, email=email, roles=role
        )

        messages.success(request, "Account created successfully")
        return redirect("login")

    return render(request, "accounts/signup.html")


def login_page(request):
    # If already logged in → redirect
    if request.user.is_authenticated:
        messages.info(request, "You are already logged in.")
        if request.user.roles == "recruiter":
            return redirect("recruiter_dashboard")
        elif request.user.roles == "jobseeker":
            return redirect("jobseeker_dashboard")

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
    messages.warning(request, "You have been Logged Out")
    return redirect("login")


@login_required(login_url="login")
def profile(request):
    user = request.user

    context = {"user": user}

    if user.roles == "jobseeker":
        context.update(
            {
                "total_applications": Application.objects.filter(
                    applicant=user
                ).count(),
                "pending_applications": Application.objects.filter(
                    applicant=user, status="pending"
                ).count(),
                "accepted_applications": Application.objects.filter(
                    applicant=user, status="accepted"
                ).count(),
                "rejected_applications": Application.objects.filter(
                    applicant=user, status="rejected"
                ).count(),
                "withdrawn_applications": Application.objects.filter(
                    applicant=user, status="withdrawn"
                ).count(),
            }
        )

    elif user.roles == "recruiter":
        context.update(
            {
                "total_jobs": Job.objects.filter(posted_by=user).count(),
                "open_jobs": Job.objects.filter(posted_by=user, status="open").count(),
                "closed_jobs": Job.objects.filter(
                    posted_by=user, status="closed"
                ).count(),
                "applications_received": Application.objects.filter(job__posted_by=user)
                .exclude(status="withdrawn")
                .count(),
            }
        )

    return render(request, "accounts/profile.html", context)
