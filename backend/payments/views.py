from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from customers.models import CustomerProfile
from bookings.models import Booking

from .models import Payment
from .serializers import PaymentSerializer
from .services import PaymentService


# =====================================
# Initiate Payment
# =====================================

class InitiatePaymentAPIView(generics.CreateAPIView):

    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):

        customer = CustomerProfile.objects.get(
            user=request.user
        )

        booking = get_object_or_404(
            Booking,
            id=request.data.get("booking")
        )

        try:

            payment = PaymentService.initiate_payment(
    customer=customer,
    booking=booking,
    gateway=request.data.get("gateway", "KHALTI"),
)

        except ValueError as e:

            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(payment)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


# =====================================
# Verify Payment
# =====================================

class VerifyPaymentAPIView(generics.GenericAPIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        customer = CustomerProfile.objects.get(
            user=request.user
        )

        payment = get_object_or_404(
            Payment,
            id=request.data.get("payment_id"),
            customer=customer,
        )

        try:

            payment = PaymentService.verify_payment(payment)

        except ValueError as e:

            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = PaymentSerializer(payment)

        return Response(serializer.data)

# =====================================
# Payment History
# =====================================

class PaymentHistoryAPIView(generics.ListAPIView):

    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        customer = CustomerProfile.objects.get(
            user=self.request.user
        )

        return Payment.objects.filter(
            customer=customer
        ).order_by("-created_at")


# =====================================
# Payment Detail
# =====================================

class PaymentDetailAPIView(generics.RetrieveAPIView):

    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        customer = CustomerProfile.objects.get(
            user=self.request.user
        )

        return Payment.objects.filter(
            customer=customer
        )