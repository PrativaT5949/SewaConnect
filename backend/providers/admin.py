from django.contrib import admin

from .models import (
    ProviderProfile,
    ProviderSkill
)

admin.site.register(ProviderProfile)
admin.site.register(ProviderSkill)