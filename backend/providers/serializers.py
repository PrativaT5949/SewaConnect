from rest_framework import serializers

from accounts.models import User
from .models import ProviderProfile
from .models import ProviderSkill

from services.models import Service
from reviews.models import Review
from services.serializers import ServiceSerializer
from reviews.serializers import ReviewSerializer

class ProviderRegisterSerializer(serializers.ModelSerializer):
    # User fields
    password = serializers.CharField(
        write_only=True,
        min_length=8
    )

    # ProviderProfile fields
    bio = serializers.CharField(required=False, allow_blank=True)

    experience_years = serializers.IntegerField()

    hourly_rate = serializers.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    address = serializers.CharField()

    latitude = serializers.DecimalField(
        max_digits=9,
        decimal_places=6
    )

    longitude = serializers.DecimalField(
        max_digits=9,
        decimal_places=6
    )

    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "password",
            "bio",
            "experience_years",
            "hourly_rate",
            "address",
            "latitude",
            "longitude",
        )
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        provider_data = {
            "bio": validated_data.pop("bio", ""),
            "experience_years": validated_data.pop("experience_years"),
            "hourly_rate": validated_data.pop("hourly_rate"),
            "address": validated_data.pop("address"),
            "latitude": validated_data.pop("latitude"),
            "longitude": validated_data.pop("longitude"),
        }

        password = validated_data.pop("password")

        user = User.objects.create_user(
            password=password,
            role=User.Roles.PROVIDER,
            **validated_data
        )

        ProviderProfile.objects.create(
            user=user,
            **provider_data
        )

        return user

    def to_representation(self, instance):
        """
        This controls the response after successful registration.
        """
        return {
            "message": "Provider registered successfully. Waiting for admin approval.",
            "user": {
                "id": instance.id,
                "email": instance.email,
                "first_name": instance.first_name,
                "last_name": instance.last_name,
                "phone_number": instance.phone_number,
                "role": instance.role,
            },
        }
class ProviderSkillSerializer(serializers.ModelSerializer):

    skill_name = serializers.CharField(
        source="skill.name",
        read_only=True
    )

    class Meta:
        model = ProviderSkill
        fields = (
            "id",
            "provider",
            "skill",
            "skill_name",
            "experience_years",
        )

        read_only_fields = (
            "provider",
            "skill_name",
        )
        # recommended to use depth=1 for nested serialization, but here we are using source to get the skill name directly.
class ProviderProfileSerializer(serializers.ModelSerializer):

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
            "approval_status",
            "address",
            "latitude",
            "longitude",
        )
        
class ProviderDetailSerializer(serializers.ModelSerializer):

    provider_name = serializers.CharField(
        source="user.first_name",
        read_only=True
    )

    services = ServiceSerializer(
        many=True,
        read_only=True
    )

    skills = ProviderSkillSerializer(
        many=True,
        read_only=True
    )

    reviews = ReviewSerializer(
        many=True,
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
            "latitude",
            "longitude",
            "services",
            "skills",
            "reviews",
        )
        
class ProviderProfileUpdateSerializer(serializers.ModelSerializer):

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
        model = ProviderProfile

        fields = (
            "first_name",
            "last_name",
            "phone_number",
            "bio",
            "experience_years",
            "hourly_rate",
            "address",
            "latitude",
            "longitude",
            "profile_picture",
        )

    def update(self, instance, validated_data):

        user_data = validated_data.pop("user")

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

        instance.bio = validated_data.get(
            "bio",
            instance.bio
        )

        instance.experience_years = validated_data.get(
            "experience_years",
            instance.experience_years
        )

        instance.hourly_rate = validated_data.get(
            "hourly_rate",
            instance.hourly_rate
        )

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

        if "profile_picture" in validated_data:
            instance.profile_picture = validated_data["profile_picture"]

        instance.save()

        return instance