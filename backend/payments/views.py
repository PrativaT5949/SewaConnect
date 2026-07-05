from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from customers.models import CustomerProfile

from .models import Payment
from .serializers import PaymentSerializer


# =====================================
# Create Payment
# =====================================

class CreatePaymentAPIView(generics.CreateAPIView):

    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):

        customer = CustomerProfile.objects.get(
            user=self.request.user
        )

        serializer.save(
            customer=customer
        )


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