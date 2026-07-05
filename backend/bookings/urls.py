from django.urls import path

from .views import (
    BookingCreateAPIView,
    CustomerBookingListAPIView,
    ProviderBookingListAPIView,
    AcceptBookingAPIView,
    RejectBookingAPIView,
    StartBookingAPIView,
    CompleteBookingAPIView,
    CancelBookingAPIView,
)

urlpatterns = [

    path(
        "create/",
        BookingCreateAPIView.as_view(),
        name="booking-create",
    ),

    path(
        "customer/",
        CustomerBookingListAPIView.as_view(),
        name="customer-bookings",
    ),

    path(
        "provider/",
        ProviderBookingListAPIView.as_view(),
        name="provider-bookings",
    ),

    path(
        "<int:pk>/accept/",
        AcceptBookingAPIView.as_view(),
        name="booking-accept",
    ),

    path(
        "<int:pk>/reject/",
        RejectBookingAPIView.as_view(),
        name="booking-reject",
    ),

    path(
        "<int:pk>/start/",
        StartBookingAPIView.as_view(),
        name="booking-start",
    ),

    path(
        "<int:pk>/complete/",
        CompleteBookingAPIView.as_view(),
        name="booking-complete",
    ),

    path(
        "<int:pk>/cancel/",
        CancelBookingAPIView.as_view(),
        name="booking-cancel",
    ),
]