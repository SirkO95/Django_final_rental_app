from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Sum

from .forms import RegisterForm
from .models import Listing, Booking


def register_view(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    form = RegisterForm(request.POST or None)

    if form.is_valid():

        user = form.save()

        login(request, user)

        messages.success(
            request,
            "Registration completed successfully."
        )

        return redirect("dashboard")

    return render(
        request,
        "account/register.html",
        {
            "form": form
        }
    )


def login_view(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:

            login(request, user)

            messages.success(
                request,
                f"Welcome back, {user.username}!"
            )

            return redirect("dashboard")

        messages.error(
            request,
            "Invalid username or password."
        )

    return render(
        request,
        "account/login.html"
    )


def logout_view(request):

    logout(request)

    messages.success(
        request,
        "You have been logged out."
    )

    return redirect("home")


def dashboard(request):

    if not request.user.is_authenticated:
        return redirect("login")

    listings = Listing.objects.filter(
        owner=request.user
    ).order_by("-created_at")

    landlord_bookings = Booking.objects.filter(
        listing__owner=request.user
    ).order_by("-created_at")

    pending_bookings = landlord_bookings.filter(
        status="pending"
    )

    confirmed_bookings = landlord_bookings.filter(
        status="confirmed"
    )

    cancelled_bookings = landlord_bookings.filter(
        status="cancelled"
    )

    completed_bookings = landlord_bookings.filter(
        status="completed"
    )

    my_bookings = Booking.objects.filter(
        tenant=request.user
    ).order_by("-created_at")

    total_views = listings.aggregate(
        total=Sum("views_count")
    )["total"] or 0

    active_bookings = confirmed_bookings.count()

    context = {
        "listings": listings,
        "my_bookings": my_bookings,
        "pending_bookings": pending_bookings,
        "confirmed_bookings": confirmed_bookings,
        "cancelled_bookings": cancelled_bookings,
        "completed_bookings": completed_bookings,
        "active_bookings": active_bookings,
        "total_views": total_views,
    }

    return render(
        request,
        "account/dashboard.html",
        context
    )