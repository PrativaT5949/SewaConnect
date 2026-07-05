# make notification automatic
from .models import Notification


def create_notification(receiver, title, message):

    Notification.objects.create(
        receiver=receiver,
        title=title,
        message=message,
    )