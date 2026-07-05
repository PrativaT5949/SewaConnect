from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from customers.models import CustomerProfile
from providers.models import ProviderProfile

from .models import Favorite
from .serializers import FavoriteSerializer

from common.pagination import StandardResultsSetPagination
from permissions.permissions import IsCustomer
class FavoriteCreateAPIView(generics.CreateAPIView):

    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated, IsCustomer]

    def perform_create(self, serializer):

        customer = CustomerProfile.objects.get(
            user=self.request.user
        )

        provider = ProviderProfile.objects.get(
            id=self.request.data["provider"]
        )

        serializer.save(
            customer=customer,
            provider=provider,
        )

# fav list API
class FavoriteListAPIView(generics.ListAPIView):

    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    def get_queryset(self):

        customer = CustomerProfile.objects.get(
            user=self.request.user
        )

        return Favorite.objects.filter(
            customer=customer
        ).order_by("-created_at")

# Remove favorite API
class FavoriteDeleteAPIView(APIView):

    permission_classes = [IsAuthenticated, IsCustomer]

    def delete(self, request, pk):

        customer = CustomerProfile.objects.get(
            user=request.user
        )

        favorite = Favorite.objects.get(
            customer=customer,
            provider_id=pk
        )

        favorite.delete()

        return Response(
            {
                "message": "Removed from favorites."
            }
        )

