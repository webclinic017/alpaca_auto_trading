from django.urls import path
from core.user.views import AccountRegisterViewV1



urlpatterns = [
    path('',AccountRegisterViewV1.as_view(),name='account-register'),
]