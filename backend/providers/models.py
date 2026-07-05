from django.db import models
from django.conf import settings


class ApprovalStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    APPROVED = "APPROVED", "Approved"
    REJECTED = "REJECTED", "Rejected"


class ProviderProfile(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="provider_profile"
    )

    bio = models.TextField(blank=True)

    experience_years = models.PositiveIntegerField(default=0)

    hourly_rate = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    profile_picture = models.ImageField(
        upload_to="providers/profile/",
        blank=True,
        null=True
    )

    citizenship_image = models.ImageField(
        upload_to="providers/citizenship/",
        blank=True,
        null=True
    )

    certificate_image = models.ImageField(
        upload_to="providers/certificate/",
        blank=True,
        null=True
    )

    address = models.CharField(max_length=255)

    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6
    )

    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6
    )

    approval_status = models.CharField(
        max_length=20,
        choices=ApprovalStatus.choices,
        default=ApprovalStatus.PENDING
    )

    average_rating = models.FloatField(default=0)

    completed_jobs = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email
    
    #skill model
class Skill(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
    )

    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
# provider skill model
class ProviderSkill(models.Model):

    provider = models.ForeignKey(
        ProviderProfile,
        on_delete=models.CASCADE,
         related_name="provider_skills"
    )

    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE,
        related_name="provider_skills"
    )


    experience_years = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = (
            "provider",
            "skill",
        )

    def __str__(self):
        return f"{self.provider.user.first_name} - {self.skill.name}"
