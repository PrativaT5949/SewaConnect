from django.urls import path

from .views import (
    CustomerRegisterAPIView,
    ProfileAPIView,
    CurrentUserAPIView,
)

urlpatterns = [
    path(
        "register/customer/",
        CustomerRegisterAPIView.as_view(),
        name="customer-register",
    ),

    path(
        "profile/",
        ProfileAPIView.as_view(),
        name="profile",
    ),
    path(
    "me/",
    CurrentUserAPIView.as_view(),
    name="current-user",
),
]