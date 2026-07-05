from rest_framework import serializers
from providers.models import ProviderProfile


class SearchProviderSerializer(serializers.ModelSerializer):

    provider_name = serializers.CharField(
        source="user.first_name",
        read_only=True
    )

    class Meta:
        model = ProviderProfile

        fields = (
            "id",
            "provider_name",
            "bio",
            "experience_years",
            "hourly_rate",
            "average_rating",
            "completed_jobs",
            "address",
        )