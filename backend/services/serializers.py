from rest_framework import serializers
from .models import Category, Service , Skill


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"


class ServiceSerializer(serializers.ModelSerializer):

    provider_name = serializers.CharField(
        source="provider.user.first_name",
        read_only=True
    )

    category_name = serializers.CharField(
        source="category.name",
        read_only=True
    )

    class Meta:
        model = Service
        fields = (
            "id",
            "provider",
            "provider_name",
            "category",
            "category_name",
            "title",
            "description",
            "price",
            "estimated_duration",
            "is_available",
            "created_at",
        )

        read_only_fields = (
            "provider",
            "provider_name",
            "category_name",
            "created_at",
        )

class SkillSerializer(serializers.ModelSerializer):

    category_name = serializers.CharField(
        source="category.name",
        read_only=True
    )

    class Meta:
        model = Skill

        fields = "__all__"