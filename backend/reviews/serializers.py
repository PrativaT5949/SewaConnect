from rest_framework import serializers

from .models import Review


class ReviewSerializer(serializers.ModelSerializer):

    customer_name = serializers.CharField(
        source="customer.user.first_name",
        read_only=True
    )

    class Meta:
        model = Review
        fields = (
            "id",
            "booking",
            "customer",
            "customer_name",
            "provider",
            "rating",
            "comment",
            "created_at",
        )

        read_only_fields = (
            "customer",
            "provider",
            "created_at",
        )