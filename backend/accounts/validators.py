import re

from rest_framework import serializers


def validate_phone(phone):

    pattern = r"^98\d{8}$"

    if not re.match(pattern, phone):
        raise serializers.ValidationError(
            "Enter a valid Nepali phone number."
        )


def validate_password(password):

    if len(password) < 8:
        raise serializers.ValidationError(
            "Password must contain at least 8 characters."
        )

    if not any(char.isupper() for char in password):
        raise serializers.ValidationError(
            "Password must contain one uppercase letter."
        )

    if not any(char.islower() for char in password):
        raise serializers.ValidationError(
            "Password must contain one lowercase letter."
        )

    if not any(char.isdigit() for char in password):
        raise serializers.ValidationError(
            "Password must contain one digit."
        )