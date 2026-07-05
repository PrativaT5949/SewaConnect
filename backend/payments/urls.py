from django.urls import path

from .views import (
    CreatePaymentAPIView,
    PaymentHistoryAPIView,
)

urlpatterns = [

    path(
        "create/",
        CreatePaymentAPIView.as_view(),
        name="create-payment",
    ),

    path(
        "history/",
        PaymentHistoryAPIView.as_view(),
        name="payment-history",
    ),
]