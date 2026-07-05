from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Notification
from .serializers import NotificationSerializer
from common.pagination import StandardResultsSetPagination

class NotificationListAPIView(generics.ListAPIView):

    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):

        return Notification.objects.filter(
            receiver=self.request.user
        )


class MarkNotificationReadAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):

        notification = Notification.objects.get(
            id=pk,
            receiver=request.user
        )

        notification.is_read = True
        notification.save()

        return Response(
            {
                "message": "Notification marked as read."
            }
        )


class MarkAllNotificationsReadAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def patch(self, request):

        Notification.objects.filter(
            receiver=request.user,
            is_read=False
        ).update(is_read=True)

        return Response(
            {
                "message": "All notifications marked as read."
            }
        )