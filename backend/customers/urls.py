from django.urls import path
from .views import( CustomerDashboardAPIView,
                   CustomerProfileUpdateAPIView,
)
urlpatterns = [

    path(
        "dashboard/",
        CustomerDashboardAPIView.as_view(),
        name="customer-dashboard",
    ),
    path(
        "profile/update/",
        CustomerProfileUpdateAPIView.as_view(),
        name="customer-profile-update",
    ),
]