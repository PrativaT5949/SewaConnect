from django.db import models


class Favorite(models.Model):

    customer = models.ForeignKey(
        "customers.CustomerProfile",
        on_delete=models.CASCADE,
        related_name="favorites"
    )

    provider = models.ForeignKey(
        "providers.ProviderProfile",
        on_delete=models.CASCADE,
        related_name="favorited_by"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = (
            "customer",
            "provider",
        )

    def __str__(self):
        return f"{self.customer.user.first_name} {self.provider.user.first_name}"