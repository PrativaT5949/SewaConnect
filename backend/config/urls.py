from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [

    # ==========================
    # Admin
    # ==========================
    path("admin/", admin.site.urls),

    # ==========================
    # Authentication
    # ==========================
    path("api/auth/", include("accounts.urls")),

    path(
        "api/auth/login/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),

    path(
        "api/auth/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),

    # ==========================
    # Services
    # ==========================
    path(
        "api/",
        include("services.urls"),
    ),

    # ==========================
    # Providers
    # ==========================
    path(
        "api/providers/",
        include("providers.urls"),
    ),

    # ==========================
    # Customers
    # ==========================
    path(
        "api/customers/",
        include("customers.urls"),
    ),

    # ==========================
    # Bookings
    # ==========================
    path(
        "api/bookings/",
        include("bookings.urls"),
    ),

    # ==========================
    # Reviews
    # ==========================
    path(
        "api/reviews/",
        include("reviews.urls"),
    ),

    # ==========================
    # Favorites
    # ==========================
    path(
        "api/favorites/",
        include("favorites.urls"),
    ),

    # ==========================
    # Search
    # ==========================
    path(
        "api/search/",
        include("search.urls"),
    ),

    # ==========================
    # Notifications
    # ==========================
    path(
        "api/notifications/",
        include("notifications.urls"),
    ),

    # ==========================
    # Swagger Documentation
    # ==========================
    path(
        "api/schema/",
        SpectacularAPIView.as_view(),
        name="schema",
    ),

    path(
        "swagger/",
        SpectacularSwaggerView.as_view(
            url_name="schema"
        ),
        name="swagger-ui",
    ),

    path(
        "redoc/",
        SpectacularRedocView.as_view(
            url_name="schema"
        ),
        name="redoc",
    ),
    path(
    "api/payments/",
    include("payments.urls"),
),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )