import uuid

from django.utils import timezone

from bookings.models import Booking

from .models import Payment, PaymentStatus


class PaymentService:

    @staticmethod
    def generate_transaction_id():

        return f"TXN-{uuid.uuid4().hex[:12].upper()}"

    @staticmethod
    def initiate_payment(customer, booking, gateway):
        
        # Prevent duplicate payment
        if Payment.objects.filter(booking=booking).exists():
            raise ValueError("Payment already exists for this booking.")
        
        transaction_id = PaymentService.generate_transaction_id()
        payment = Payment.objects.create(
    booking=booking,
    customer=customer,
    amount=booking.total_price,
    gateway=gateway,
    transaction_id=transaction_id,
    status=PaymentStatus.PENDING,
)

        return payment

    @staticmethod
    def verify_payment(payment):

     if payment.status == PaymentStatus.SUCCESS:
        raise ValueError("Payment has already been verified.")

     payment.status = PaymentStatus.SUCCESS
     payment.payment_reference = payment.transaction_id
     payment.paid_at = timezone.now()
     payment.save()

    # Update booking status
     payment.booking.status = Booking.BookingStatus.ACCEPTED
     payment.booking.save()

     return payment