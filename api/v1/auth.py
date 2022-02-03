from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from core.user.views import RevokeToken, PairTokenView


urlpatterns = [
    path("", PairTokenView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("revoke/", RevokeToken.as_view(), name="token_revoke"),
]