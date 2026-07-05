from rest_framework import serializers

from .models import Booking


class BookingSerializer(serializers.ModelSerializer):

    customer_name = serializers.CharField(
        source="customer.user.first_name",
        read_only=True
    )

    provider_name = serializers.CharField(
        source="provider.user.first_name",
        read_only=True
    )

    service_name = serializers.CharField(
        source="service.title",
        read_only=True
    )
    
    class Meta:
        model = Booking

        fields = (
            "id",
            "customer",
            "customer_name",
            "provider",
            "provider_name",
            "service",
            "service_name",
            "booking_date",
            "booking_time",
            "address",
            "latitude",
            "longitude",
            "note",
            "total_price",
            "status",
            "created_at",
        )

        read_only_fields = (
            "customer",
            "provider",          
            "customer_name",
            "provider_name",
            "service_name",
            "status",
            "created_at",
        ) 
        
