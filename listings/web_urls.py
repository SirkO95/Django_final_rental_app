from django.urls import path

from .html_views import (
    home,
    listing_list,
    listing_detail,
    create_listing,
    edit_listing,
    delete_listing,
    create_booking,
    my_bookings,
    landlord_bookings,
    confirm_booking,
    cancel_booking,
    create_review,
)

from .account_views import (
    login_view,
    register_view,
    logout_view,
    dashboard,
)

urlpatterns = [

    path("", home, name="home"),

    path("login/", login_view, name="login"),
    path("register/", register_view, name="register"),
    path("logout/", logout_view, name="logout"),

    path("dashboard/", dashboard, name="dashboard"),

    path("listings/", listing_list, name="listing_list"),

    path("listing/create/", create_listing, name="create_listing"),

    path("listing/<int:pk>/", listing_detail, name="listing_detail"),

    path("listing/<int:pk>/edit/", edit_listing, name="edit_listing"),

    path("listing/<int:pk>/delete/", delete_listing, name="delete_listing"),

    path("listing/<int:pk>/book/", create_booking, name="create_booking"),

    path("listing/<int:pk>/review/", create_review, name="create_review"),

    path("my-bookings/", my_bookings, name="my_bookings"),

    path(
        "landlord-bookings/",
        landlord_bookings,
        name="landlord_bookings"
    ),

    path(
        "booking/<int:pk>/confirm/",
        confirm_booking,
        name="confirm_booking"
    ),

    path(
        "booking/<int:pk>/cancel/",
        cancel_booking,
        name="cancel_booking"
    ),

]