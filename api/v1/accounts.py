from django.urls import path
from core.user.views import AccountRegisterViewV1
from core.accounts.views import AccounUpgradeViewV1


urlpatterns = [
    path('',AccountRegisterViewV1.as_view(),name='account-register'),
    path('upgrade/',AccounUpgradeViewV1.as_view(),name='account-upgrade'),
]