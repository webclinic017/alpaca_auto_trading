from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
urlpatterns =[
    path("swagger/", SpectacularAPIView.as_view(api_version='v1'), name="schemav1"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schemav1"), name="swagger-ui"),
    path("", SpectacularRedocView.as_view(url_name="schemav1"), name="redocv1"),
    path('auth/', include('api.v1.auth')),
    path('accounts/', include('api.v1.accounts')),
]