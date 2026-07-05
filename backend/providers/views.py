from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.db.models import Sum

from bookings.models import Booking
from .models import ProviderProfile, ProviderSkill
from .serializers import (
    ProviderRegisterSerializer,
    ProviderSkillSerializer,
    ProviderProfileSerializer,
    ProviderDetailSerializer,
    ProviderProfileUpdateSerializer,
)
from .utils import haversine_distance
from common.pagination import StandardResultsSetPagination
from permissions.permissions import IsProvider
class ProviderRegisterAPIView(generics.CreateAPIView):
    serializer_class = ProviderRegisterSerializer


class ProviderSkillCreateAPIView(generics.CreateAPIView):

    serializer_class = ProviderSkillSerializer
    permission_classes = [IsAuthenticated, IsProvider]

    def perform_create(self, serializer):
        provider = ProviderProfile.objects.get(
            user=self.request.user
        )

        serializer.save(provider=provider)


class ProviderRecommendationAPIView(APIView):

    def get(self, request):

        category_id = request.GET.get("category")
        customer_lat = request.GET.get("latitude")
        customer_lon = request.GET.get("longitude")

        min_rating = request.GET.get("min_rating")
        max_price = request.GET.get("max_price")
        sort = request.GET.get("sort")

        # Convert query params
        if min_rating:
            min_rating = float(min_rating)

        if max_price:
            max_price = float(max_price)

        # Base queryset
        providers = ProviderProfile.objects.filter(
            approval_status="APPROVED"
        )

        # Content-Based Filtering
        if category_id:
            providers = providers.filter(
                services__category_id=category_id,
                services__is_available=True
            ).distinct()

        # Rating Filter
        if min_rating:
            providers = providers.filter(
                average_rating__gte=min_rating
            )

        # Price Filter
        if max_price:
            providers = providers.filter(
                hourly_rate__lte=max_price
            )

        providers = list(providers)

        if not providers:
            return Response([])

        # ----------------------------
        # Calculate Distances
        # ----------------------------

        distances = []

        for provider in providers:

            if customer_lat and customer_lon:
                distance = haversine_distance(
                    customer_lat,
                    customer_lon,
                    provider.latitude,
                    provider.longitude,
                )
            else:
                distance = 0

            distances.append(distance)

        highest_distance = max(distances) if distances else 1

        highest_jobs = max(
            [p.completed_jobs for p in providers],
            default=1
        )

        highest_price = max(
            [float(p.hourly_rate) for p in providers],
            default=1
        )

        recommendations = []

        # ----------------------------
        # Weighted Scoring Algorithm
        # ----------------------------

        for index, provider in enumerate(providers):

            distance = distances[index]

            rating_score = (
                provider.average_rating / 5
            ) * 100

            distance_score = (
                ((highest_distance - distance) / highest_distance) * 100
                if highest_distance > 0 else 100
            )

            jobs_score = (
                (provider.completed_jobs / highest_jobs) * 100
                if highest_jobs > 0 else 0
            )

            price_score = (
                ((highest_price - float(provider.hourly_rate)) / highest_price) * 100
                if highest_price > 0 else 100
            )

            recommendation_score = (
                (rating_score * 0.40)
                + (distance_score * 0.30)
                + (jobs_score * 0.20)
                + (price_score * 0.10)
            )

            provider_data = ProviderProfileSerializer(provider).data

            provider_data["distance_km"] = round(distance, 2)
            provider_data["recommendation_score"] = round(
                recommendation_score,
                2
            )

            recommendations.append(provider_data)

        # ----------------------------
        # Sorting
        # ----------------------------

        if sort == "distance":
            recommendations.sort(
                key=lambda x: x["distance_km"]
            )

        elif sort == "rating":
            recommendations.sort(
                key=lambda x: x["average_rating"],
                reverse=True
            )

        elif sort == "price":
            recommendations.sort(
                key=lambda x: float(x["hourly_rate"])
            )

        else:
            recommendations.sort(
                key=lambda x: x["recommendation_score"],
                reverse=True
            )

        paginator = StandardResultsSetPagination()

        page = paginator.paginate_queryset(
              recommendations,
              request
)

        return paginator.get_paginated_response(page)

class ProviderDetailAPIView(generics.RetrieveAPIView):

    queryset = ProviderProfile.objects.all()

    serializer_class = ProviderDetailSerializer
    

class ProviderDashboardAPIView(APIView):

    permission_classes = [IsAuthenticated , IsProvider]

    def get(self, request):

        provider = ProviderProfile.objects.get(
            user=request.user
        )

        bookings = Booking.objects.filter(
            provider=provider
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

            "average_rating": provider.average_rating,

            "completed_jobs": provider.completed_jobs,

            "total_earnings": bookings.filter(
                status="COMPLETED"
            ).aggregate(
                total=Sum("total_price")
            )["total"] or 0,
        }

        return Response(dashboard)

class ProviderProfileUpdateAPIView(generics.UpdateAPIView):

    serializer_class = ProviderProfileUpdateSerializer
    permission_classes = [IsAuthenticated, IsProvider]

    def get_object(self):

        return ProviderProfile.objects.get(
            user=self.request.user
        )