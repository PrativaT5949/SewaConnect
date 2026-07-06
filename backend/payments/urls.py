from django.urls import path

from .views import (
    InitiatePaymentAPIView,
    VerifyPaymentAPIView,
    PaymentHistoryAPIView,
    PaymentDetailAPIView,
)

urlpatterns = [

    path(
        "initiate/",
        InitiatePaymentAPIView.as_view(),
        name="payment-initiate",
    ),

    path(
        "verify/",
        VerifyPaymentAPIView.as_view(),
        name="payment-verify",
    ),

    path(
        "history/",
        PaymentHistoryAPIView.as_view(),
        name="payment-history",
    ),

    path(
        "<int:pk>/",
        PaymentDetailAPIView.as_view(),
        name="payment-detail",
    ),
]