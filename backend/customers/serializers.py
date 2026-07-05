from rest_framework import serializers
from .models import CustomerProfile


class CustomerProfileUpdateSerializer(serializers.ModelSerializer):

    first_name = serializers.CharField(
        source="user.first_name"
    )

    last_name = serializers.CharField(
        source="user.last_name"
    )

    phone_number = serializers.CharField(
        source="user.phone_number"
    )

    class Meta:
        model = CustomerProfile

        fields = (
            "first_name",
            "last_name",
            "phone_number",
            "address",
            "latitude",
            "longitude",
        )

    def update(self, instance, validated_data):

        user_data = validated_data.pop("user", {})

        user = instance.user

        user.first_name = user_data.get(
            "first_name",
            user.first_name
        )

        user.last_name = user_data.get(
            "last_name",
            user.last_name
        )

        user.phone_number = user_data.get(
            "phone_number",
            user.phone_number
        )

        user.save()

        instance.address = validated_data.get(
            "address",
            instance.address
        )

        instance.latitude = validated_data.get(
            "latitude",
            instance.latitude
        )

        instance.longitude = validated_data.get(
            "longitude",
            instance.longitude
        )

        instance.save()

        return instance