from django.urls import path

from .views import (
    CategoryListAPIView,
    CategoryCreateAPIView,
    SkillListAPIView,
    SkillCreateAPIView,
    ServiceCreateAPIView,
    ServiceListAPIView,
)

urlpatterns = [
    path(
        "categories/",
        CategoryListAPIView.as_view(),
        name="category-list",
    ),

    path(
        "categories/create/",
        CategoryCreateAPIView.as_view(),
        name="category-create",
    ),
    path(
        "skills/",
        SkillListAPIView.as_view(),
    ),

    path(
        "skills/create/",
        SkillCreateAPIView.as_view(),
    ),
    
    path(
        "services/",
        ServiceListAPIView.as_view(),
        name="service-list",
    ),
    path(
        "services/create/",
        ServiceCreateAPIView.as_view(),
        name="service-create",
    ),
]