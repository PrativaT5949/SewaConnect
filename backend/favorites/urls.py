from django.urls import path

from .views import (
    FavoriteCreateAPIView,
    FavoriteListAPIView,
    FavoriteDeleteAPIView,
)

urlpatterns = [

    path(
        "add/",
        FavoriteCreateAPIView.as_view(),
    ),

    path(
        "",
        FavoriteListAPIView.as_view(),
    ),

    path(
        "<int:pk>/remove/",
        FavoriteDeleteAPIView.as_view(),
    ),
]