from django.db.models import Avg

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from customers.models import CustomerProfile
from bookings.models import Booking

from .models import Review
from .serializers import ReviewSerializer

from common.pagination import StandardResultsSetPagination

from permissions.permissions import IsCustomer
# ======================================
# Create Review
# ======================================

class CreateReviewAPIView(generics.CreateAPIView):

    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated,IsCustomer]

    def perform_create(self, serializer):

        customer = CustomerProfile.objects.get(
            user=self.request.user
        )

        booking = Booking.objects.get(
            id=self.request.data["booking"]
        )

        # Booking must belong to the customer
        if booking.customer != customer:
            raise PermissionError(
                "This booking does not belong to you."
            )

        # Booking must be completed
        if booking.status != Booking.BookingStatus.COMPLETED:
            raise serializer.ValidationError(
                "Booking is not completed."
            )

        # Prevent duplicate review
        if Review.objects.filter(booking=booking).exists():
            raise serializer.ValidationError(
                "You have already reviewed this booking."
            )

        serializer.save(
            booking=booking,
            customer=customer,
            provider=booking.provider,
        )

        # Update provider average rating
        avg_rating = Review.objects.filter(
            provider=booking.provider
        ).aggregate(
            Avg("rating")
        )["rating__avg"]

        booking.provider.average_rating = round(avg_rating, 2)
        booking.provider.save()


# ======================================
# Provider Review List
# ======================================

class ProviderReviewListAPIView(generics.ListAPIView):

    serializer_class = ReviewSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):

        provider_id = self.kwargs["provider_id"]

        return Review.objects.filter(
            provider_id=provider_id
        ).order_by("-created_at")