from django.urls import path

from .views import( ProviderRegisterAPIView, ProviderSkillCreateAPIView,
                   ProviderRecommendationAPIView,ProviderDashboardAPIView,
                   ProviderDetailAPIView,ProviderProfileUpdateAPIView,
)

urlpatterns = [
    path(
        "register/",
        ProviderRegisterAPIView.as_view(),
        name="provider-register",
    ),
    path(
        "skills/add/",
        ProviderSkillCreateAPIView.as_view(),
        name="provider-skill-create",
    ),
        path(
        "recommendations/",
        ProviderRecommendationAPIView.as_view(),
        name="provider-recommendations",
    ),
        path(
    "dashboard/",
    ProviderDashboardAPIView.as_view(),
    name="provider-dashboard",
),
  path(
    "<int:pk>/",
    ProviderDetailAPIView.as_view(),
    name="provider-detail",
),   
    path(
    "profile/update/",
    ProviderProfileUpdateAPIView.as_view(),
    name="provider-profile-update",
), 
]