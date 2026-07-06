from rest_framework import serializers

from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:

        model = Payment

        fields = (
            "id",
            "booking",
            "customer",
            "amount",
            "gateway",
            "transaction_id",
            "payment_reference",
            "status",
            "paid_at",
            "created_at",
        )

        read_only_fields = (
            "customer",
            "transaction_id",
            "payment_reference",
            "status",
            "paid_at",
            "created_at",
        )