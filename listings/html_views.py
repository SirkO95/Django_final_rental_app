from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import (
    Listing,
    Booking,
    Review,
    SearchHistory,
    ViewHistory,
)
from .forms import ListingForm


def home(request):
    latest = Listing.objects.filter(
        is_active=True
    ).order_by("-created_at")[:6]

    popular = Listing.objects.filter(
        is_active=True
    ).order_by("-views_count")[:6]

    return render(
        request,
        "home/index.html",
        {
            "latest": latest,
            "popular": popular,
        },
    )


def listing_list(request):

    listings = Listing.objects.filter(is_active=True)

    search = request.GET.get("search")
    location = request.GET.get("location")
    housing_type = request.GET.get("type")
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    rooms = request.GET.get("rooms")
    sort = request.GET.get("sort")

    if search:

        listings = listings.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search)
        )

        if request.user.is_authenticated:
            SearchHistory.objects.create(
                user=request.user,
                query=search
            )
    if location:
        listings = listings.filter(
            location__icontains=location
        )

    if housing_type:
        listings = listings.filter(
            housing_type=housing_type
        )

    if min_price:
        listings = listings.filter(
            price__gte=min_price
        )

    if max_price:
        listings = listings.filter(
            price__lte=max_price
        )

    if rooms:
        listings = listings.filter(
            rooms=rooms
        )

    if sort == "price_asc":

        listings = listings.order_by("price")

    elif sort == "price_desc":

        listings = listings.order_by("-price")

    elif sort == "oldest":

        listings = listings.order_by("created_at")

    elif sort == "popular":

        listings = listings.order_by("-views_count")

    else:

        listings = listings.order_by("-created_at")

    return render(
        request,
        "listings/list.html",
        {
            "listings": listings,
        },
    )


def listing_detail(request, pk):

    listing = get_object_or_404(
        Listing,
        pk=pk
    )

    listing.views_count += 1
    listing.save(update_fields=["views_count"])

    if request.user.is_authenticated:
        ViewHistory.objects.create(
            user=request.user,
            listing=listing
        )

    return render(
        request,
        "listings/detail.html",
        {
            "listing": listing
        },
    )


@login_required
def create_listing(request):

    if not request.user.is_landlord:

        messages.error(
            request,
            "Only landlords can create listings."
        )

        return redirect("listing_list")

    form = ListingForm(
        request.POST or None,
        request.FILES or None
    )

    if form.is_valid():

        listing = form.save(commit=False)

        listing.owner = request.user

        listing.save()

        messages.success(
            request,
            "Listing created successfully."
        )

        return redirect(
            "listing_detail",
            pk=listing.pk
        )

    return render(
        request,
        "listings/create.html",
        {
            "form": form
        }
    )


@login_required
def edit_listing(request, pk):

    listing = get_object_or_404(
        Listing,
        pk=pk,
        owner=request.user
    )

    form = ListingForm(
        request.POST or None,
        request.FILES or None,
        instance=listing
    )

    if form.is_valid():

        form.save()

        messages.success(
            request,
            "Listing updated successfully."
        )

        return redirect(
            "listing_detail",
            pk=listing.pk
        )

    return render(
        request,
        "listings/create.html",
        {
            "form": form
        }
    )


@login_required
def delete_listing(request, pk):

    listing = get_object_or_404(
        Listing,
        pk=pk,
        owner=request.user
    )

    if request.method == "POST":

        listing.delete()

        messages.success(
            request,
            "Listing deleted successfully."
        )

        return redirect("dashboard")

    return render(
        request,
        "listings/delete.html",
        {
            "listing": listing
        }
    )


@login_required
def create_booking(request, pk):

    listing = get_object_or_404(
        Listing,
        pk=pk,
        is_active=True
    )

    if request.user == listing.owner:

        messages.error(
            request,
            "You cannot book your own property."
        )

        return redirect(
            "listing_detail",
            pk=listing.pk
        )

    if request.method == "POST":

        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")

        conflict = Booking.objects.filter(
            listing=listing,
            status="confirmed",
            start_date__lte=end_date,
            end_date__gte=start_date,
        ).exists()

        if conflict:

            messages.error(
                request,
                "Selected dates are already booked."
            )

            return redirect(
                "listing_detail",
                pk=listing.pk
            )

        Booking.objects.create(
            listing=listing,
            tenant=request.user,
            start_date=start_date,
            end_date=end_date,
            status="pending"
        )

        messages.success(
            request,
            "Booking request has been sent."
        )

        return redirect("my_bookings")

    return render(
        request,
        "bookings/create.html",
        {
            "listing": listing
        }
    )


@login_required
def my_bookings(request):

    bookings = Booking.objects.filter(
        tenant=request.user
    ).order_by("-created_at")

    return render(
        request,
        "bookings/my_bookings.html",
        {
            "bookings": bookings
        }
    )
@login_required
def landlord_bookings(request):

    bookings = Booking.objects.filter(
        listing__owner=request.user
    ).order_by("-created_at")

    return render(
        request,
        "bookings/landlord_bookings.html",
        {
            "bookings": bookings
        }
    )


@login_required
def confirm_booking(request, pk):

    booking = get_object_or_404(
        Booking,
        pk=pk,
        listing__owner=request.user
    )

    booking.status = "confirmed"
    booking.save()

    messages.success(
        request,
        "Booking confirmed."
    )

    return redirect("landlord_bookings")


@login_required
def cancel_booking(request, pk):

    booking = get_object_or_404(
        Booking,
        pk=pk,
        listing__owner=request.user
    )

    booking.status = "cancelled"
    booking.save()

    messages.success(
        request,
        "Booking cancelled."
    )

    return redirect("landlord_bookings")
@login_required
def create_review(request, pk):

    listing = get_object_or_404(
        Listing,
        pk=pk
    )

    booking = Booking.objects.filter(
        listing=listing,
        tenant=request.user,
        status="completed"
    ).exists()

    if not booking:

        messages.error(
            request,
            "You can leave a review only after completing your stay."
        )

        return redirect(
            "listing_detail",
            pk=listing.pk
        )

    review_exists = Review.objects.filter(
        listing=listing,
        tenant=request.user
    ).exists()

    if review_exists:

        messages.error(
            request,
            "You have already left a review for this property."
        )

        return redirect(
            "listing_detail",
            pk=listing.pk
        )

    if request.method == "POST":

        rating = request.POST.get("rating")
        comment = request.POST.get("comment")

        Review.objects.create(
            listing=listing,
            tenant=request.user,
            rating=rating,
            comment=comment
        )

        messages.success(
            request,
            "Thank you! Your review has been added."
        )

        return redirect(
            "listing_detail",
            pk=listing.pk
        )

    return render(
        request,
        "reviews/create.html",
        {
            "listing": listing
        }
    )