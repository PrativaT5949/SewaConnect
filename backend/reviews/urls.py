from django.urls import path

from .views import (CreateReviewAPIView,
                    ProviderReviewListAPIView)

urlpatterns = [
    path(
        "create/",
        CreateReviewAPIView.as_view(),
        name="create-review",
    ),
      path(
        "provider/<int:provider_id>/",
        ProviderReviewListAPIView.as_view(),
        name="provider-reviews",
    ),
]