from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from providers.models import ProviderProfile

from .models import Category, Service , Skill
from .serializers import CategorySerializer, ServiceSerializer , SkillSerializer


class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer


class CategoryCreateAPIView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ServiceListAPIView(generics.ListAPIView):
    queryset = Service.objects.filter(is_available=True)
    serializer_class = ServiceSerializer

class SkillListAPIView(generics.ListAPIView):

    queryset = Skill.objects.all()

    serializer_class = SkillSerializer


class SkillCreateAPIView(generics.CreateAPIView):

    queryset = Skill.objects.all()

    serializer_class = SkillSerializer


class ServiceCreateAPIView(generics.CreateAPIView):
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        provider = ProviderProfile.objects.get(
            user=self.request.user
        )
        serializer.save(provider=provider)