from rest_framework import serializers

from .models import Favorite


class FavoriteSerializer(serializers.ModelSerializer):

    provider_name = serializers.CharField(
        source="provider.user.first_name",
        read_only=True
    )

    class Meta:

        model = Favorite

        fields = (
            "id",
            "provider",
            "provider_name",
            "created_at",
        )