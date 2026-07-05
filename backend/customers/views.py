from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import CustomerProfileUpdateSerializer
from bookings.models import Booking
from .models import CustomerProfile
from permissions.permissions import IsCustomer

from django.db.models import Sum

class CustomerDashboardAPIView(APIView):

    permission_classes = [IsAuthenticated, IsCustomer]

    def get(self, request):

        customer = CustomerProfile.objects.get(
            user=request.user
        )

        bookings = Booking.objects.filter(
            customer=customer
        )

        dashboard = {
            "total_bookings": bookings.count(),

            "pending_bookings": bookings.filter(
                status="PENDING"
            ).count(),

            "accepted_bookings": bookings.filter(
                status="ACCEPTED"
            ).count(),

            "completed_bookings": bookings.filter(
                status="COMPLETED"
            ).count(),

            "cancelled_bookings": bookings.filter(
                status="CANCELLED"
            ).count(),

            "total_spent": bookings.filter(
                status="COMPLETED"
            ).aggregate(
                total=Sum("total_price")
            )["total"] or 0,
        }

        return Response(dashboard)

class CustomerProfileUpdateAPIView(generics.UpdateAPIView):

    serializer_class = CustomerProfileUpdateSerializer
    permission_classes = [IsAuthenticated, IsCustomer]

    def get_object(self):
        return CustomerProfile.objects.get(
            user=self.request.user
        )