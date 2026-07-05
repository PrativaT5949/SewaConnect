from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import (
    CustomerRegisterSerializer,
    ProfileSerializer,
    CurrentUserSerializer,
)


class CustomerRegisterAPIView(generics.CreateAPIView):
    serializer_class = CustomerRegisterSerializer


class ProfileAPIView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    
class CurrentUserAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        serializer = CurrentUserSerializer(request.user)

        return Response(serializer.data)