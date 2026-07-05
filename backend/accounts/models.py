from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):

    class Roles(models.TextChoices):
        CUSTOMER = "CUSTOMER", "Customer"
        PROVIDER = "PROVIDER", "Provider"
        ADMIN = "ADMIN", "Admin"

    email = models.EmailField(unique=True)

    first_name = models.CharField(max_length=100)

    last_name = models.CharField(max_length=100)

    phone_number = models.CharField(
        max_length=15,
        unique=True,
    )

    role = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.CUSTOMER,
    )

    is_active = models.BooleanField(default=True)

    is_staff = models.BooleanField(default=False)

    is_verified = models.BooleanField(default=False)

    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
        "phone_number",
    ]

    def __str__(self):
        return self.email