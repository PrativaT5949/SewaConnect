from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from customers.models import CustomerProfile
from providers.models import ProviderProfile
from services.models import Service

from .models import Booking
from .serializers import BookingSerializer

from notifications.utils import create_notification

from common.pagination import StandardResultsSetPagination
from permissions.permissions import IsCustomer,IsProvider
# =====================================================
# Create Booking
# =====================================================

class BookingCreateAPIView(generics.CreateAPIView):

    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated, IsCustomer]  # Only customers can create bookings

    def perform_create(self, serializer):

        customer = CustomerProfile.objects.get(
            user=self.request.user
        )

        service = Service.objects.get(
            id=self.request.data["service"]
        )

        provider = service.provider

        booking = serializer.save(
            customer=customer,
            provider=provider,
        )

        create_notification(
            receiver=provider.user,
            title="New Booking",
            message=f"{customer.user.first_name} booked your service."
        )


# =====================================================
# Customer Booking List
# =====================================================

class CustomerBookingListAPIView(generics.ListAPIView):

    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated, IsCustomer]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):

        customer = CustomerProfile.objects.get(
            user=self.request.user
        )

        return Booking.objects.filter(
            customer=customer
        )


# =====================================================
# Provider Booking List
# =====================================================

class ProviderBookingListAPIView(generics.ListAPIView):

    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated, IsProvider]
    pagination_class = StandardResultsSetPagination
    def get_queryset(self):

        provider = ProviderProfile.objects.get(
            user=self.request.user
        )

        return Booking.objects.filter(
            provider=provider
        )


# =====================================================
# Cancel Booking
# =====================================================

class CancelBookingAPIView(APIView):

    permission_classes = [IsAuthenticated, IsCustomer]

    def patch(self, request, pk):

        customer = CustomerProfile.objects.get(
            user=request.user
        )

        booking = Booking.objects.get(
            id=pk,
            customer=customer
        )

        if booking.status != Booking.BookingStatus.PENDING:
            return Response(
                {"error": "Only pending bookings can be cancelled."},
                status=status.HTTP_400_BAD_REQUEST
            )

        booking.status = Booking.BookingStatus.CANCELLED
        booking.save()

        create_notification(
            receiver=booking.provider.user,
            title="Booking Cancelled",
            message=f"{customer.user.first_name} cancelled the booking."
        )

        return Response(
            {"message": "Booking cancelled successfully."}
        )


# =====================================================
# Accept Booking
# =====================================================

class AcceptBookingAPIView(APIView):

    permission_classes = [IsAuthenticated, IsProvider]

    def patch(self, request, pk):

        provider = ProviderProfile.objects.get(
            user=request.user
        )

        booking = Booking.objects.get(
            id=pk,
            provider=provider
        )

        if booking.status != Booking.BookingStatus.PENDING:
            return Response(
                {"error": "Booking cannot be accepted."},
                status=status.HTTP_400_BAD_REQUEST
            )

        booking.status = Booking.BookingStatus.ACCEPTED
        booking.save()

        create_notification(
            receiver=booking.customer.user,
            title="Booking Accepted",
            message=f"{provider.user.first_name} accepted your booking."
        )

        return Response(
            {"message": "Booking accepted successfully."}
        )


# =====================================================
# Reject Booking
# =====================================================

class RejectBookingAPIView(APIView):

    permission_classes = [IsAuthenticated, IsProvider]

    def patch(self, request, pk):

        provider = ProviderProfile.objects.get(
            user=request.user
        )

        booking = Booking.objects.get(
            id=pk,
            provider=provider
        )

        if booking.status != Booking.BookingStatus.PENDING:
            return Response(
                {"error": "Booking cannot be rejected."},
                status=status.HTTP_400_BAD_REQUEST
            )

        booking.status = Booking.BookingStatus.REJECTED
        booking.save()

        create_notification(
            receiver=booking.customer.user,
            title="Booking Rejected",
            message=f"{provider.user.first_name} rejected your booking."
        )

        return Response(
            {"message": "Booking rejected successfully."}
        )


# =====================================================
# Start Booking
# =====================================================

class StartBookingAPIView(APIView):

    permission_classes = [IsAuthenticated, IsProvider]

    def patch(self, request, pk):

        provider = ProviderProfile.objects.get(
            user=request.user
        )

        booking = Booking.objects.get(
            id=pk,
            provider=provider
        )

        if booking.status != Booking.BookingStatus.ACCEPTED:
            return Response(
                {"error": "Only accepted bookings can be started."},
                status=status.HTTP_400_BAD_REQUEST
            )

        booking.status = Booking.BookingStatus.IN_PROGRESS
        booking.save()

        create_notification(
            receiver=booking.customer.user,
            title="Service Started",
            message=f"{provider.user.first_name} has started your service."
        )

        return Response(
            {"message": "Service started successfully."}
        )


# =====================================================
# Complete Booking
# =====================================================

class CompleteBookingAPIView(APIView):

    permission_classes = [IsAuthenticated, IsProvider]

    def patch(self, request, pk):

        provider = ProviderProfile.objects.get(
            user=request.user
        )

        booking = Booking.objects.get(
            id=pk,
            provider=provider
        )

        if booking.status != Booking.BookingStatus.IN_PROGRESS:
            return Response(
                {"error": "Booking is not in progress."},
                status=status.HTTP_400_BAD_REQUEST
            )

        booking.status = Booking.BookingStatus.COMPLETED
        booking.save()

        provider.completed_jobs += 1
        provider.save()

        create_notification(
            receiver=booking.customer.user,
            title="Service Completed",
            message=f"{provider.user.first_name} completed your service."
        )

        return Response(
            {"message": "Booking completed successfully."}
        )