from rest_framework import serializers

from .models import User
from customers.models import CustomerProfile
from providers.models import ProviderProfile


class CustomerRegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        min_length=8
    )

    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "password",
        )

    def create(self, validated_data):

        password = validated_data.pop("password")

        user = User.objects.create_user(
            password=password,
            role=User.Roles.CUSTOMER,
            **validated_data
        )

        CustomerProfile.objects.create(
            user=user
        )

        return user


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "role",
        )

    def to_representation(self, instance):

        data = super().to_representation(instance)

        if instance.role == User.Roles.CUSTOMER:

            try:
                profile = instance.customer_profile

                data["profile"] = {
                    "address": profile.address,
                    "latitude": profile.latitude,
                    "longitude": profile.longitude,
                    "profile_picture": (
                        profile.profile_picture.url
                        if profile.profile_picture
                        else None
                    ),
                }

            except CustomerProfile.DoesNotExist:
                data["profile"] = None

        elif instance.role == User.Roles.PROVIDER:

            try:
                profile = instance.provider_profile

                data["profile"] = {
                    "bio": profile.bio,
                    "experience_years": profile.experience_years,
                    "hourly_rate": str(profile.hourly_rate),
                    "average_rating": profile.average_rating,
                    "completed_jobs": profile.completed_jobs,
                    "approval_status": profile.approval_status,
                    "address": profile.address,
                    "latitude": profile.latitude,
                    "longitude": profile.longitude,
                    "profile_picture": (
                        profile.profile_picture.url
                        if profile.profile_picture
                        else None
                    ),
                }

            except ProviderProfile.DoesNotExist:
                data["profile"] = None

        return data



class CurrentUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "role",
            "is_verified",
        )