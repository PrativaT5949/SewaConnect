from django.db import models

from customers.models import CustomerProfile
from bookings.models import Booking


class PaymentStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    SUCCESS = "SUCCESS", "Success"
    FAILED = "FAILED", "Failed"


class PaymentGateway(models.TextChoices):
    KHALTI = "KHALTI", "Khalti"
    ESEWA = "ESEWA", "eSewa"


class Payment(models.Model):

    booking = models.OneToOneField(
        Booking,
        on_delete=models.CASCADE,
        related_name="payment",
    )

    customer = models.ForeignKey(
        CustomerProfile,
        on_delete=models.CASCADE,
        related_name="payments",
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    gateway = models.CharField(
        max_length=20,
        choices=PaymentGateway.choices,
        default=PaymentGateway.KHALTI,
    )

    transaction_id = models.CharField(
    max_length=255,
    unique=True,
    blank=True,
    null=True,
)

    payment_reference = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING,
    )

    paid_at = models.DateTimeField(
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return f"{self.transaction_id} - {self.status}"