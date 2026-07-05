from django.urls import path

from .views import SearchProviderAPIView

urlpatterns = [

    path(
        "",
        SearchProviderAPIView.as_view(),
        name="provider-search",
    ),

]