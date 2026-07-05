from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.response import Response

from providers.models import ProviderProfile

from .serializers import SearchProviderSerializer


class SearchProviderAPIView(APIView):

    def get(self, request):

        q = request.GET.get("q")

        category = request.GET.get("category")

        city = request.GET.get("city")

        skill = request.GET.get("skill")

        min_rating = request.GET.get("min_rating")

        max_price = request.GET.get("max_price")

        providers = ProviderProfile.objects.filter(
            approval_status="APPROVED"
        )

        # -------------------------
        # Keyword Search
        # -------------------------

        if q:

            providers = providers.filter(

                Q(user__first_name__icontains=q)

                | Q(user__last_name__icontains=q)

                | Q(bio__icontains=q)

                | Q(address__icontains=q)

                | Q(services__title__icontains=q)

                | Q(provider_skills__skill__name__icontains=q)

            ).distinct()

        # -------------------------
        # Category
        # -------------------------

        if category:

            providers = providers.filter(
                services__category_id=category
            ).distinct()

        # -------------------------
        # Skill
        # -------------------------

        if skill:

            providers = providers.filter(
                provider_skills__skill__name__icontains=skill
            ).distinct()

        # -------------------------
        # City
        # -------------------------

        if city:

            providers = providers.filter(
                address__icontains=city
            )

        # -------------------------
        # Rating
        # -------------------------

        if min_rating:

            providers = providers.filter(
                average_rating__gte=min_rating
            )

        # -------------------------
        # Price
        # -------------------------

        if max_price:

            providers = providers.filter(
                hourly_rate__lte=max_price
            )

        serializer = SearchProviderSerializer(
            providers,
            many=True
        )

        return Response(serializer.data)