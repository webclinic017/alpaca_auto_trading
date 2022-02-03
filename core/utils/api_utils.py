from rest_framework import serializers,permissions,status
from enum import Enum
from rest_framework.exceptions import APIException


class IsPostOrIsAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        # allow all POST requests
        if request.method == "POST":
            return True

        # Otherwise, only allow authenticated requests
        # Post Django 1.10, 'is_authenticated' is a read-only attribute
        return request.user and request.user.is_authenticated


class RegiesterRepsonse(Enum):
    ACCOUNT_EXIST = "Account with this email already exists"
    ACCOUNT_CREATED = "Account created successfully"
    EMAIL_NOT_VALID = "email is not a valid email address"
    PASSWORD_TO_COMMON = "Password is to common"
    PASSWORD_SIMILIAR = "Password is similiar to username/email"

class AuthorizationEnum(Enum):
    PERMISSIONS_ERROR ='User is not Registered or has permission'


class ApiErrorMessage(Enum):
    ERROR_429 = "Too many request"
    ERROR_400 = "Bad request / invaid payload"


class DefaultMessageSerializer(serializers.Serializer):
    detail = serializers.CharField()
    

class AuthorizationException(APIException):
    """
    change 401 to 403
    """
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = {'detail': AuthorizationEnum.PERMISSIONS_ERROR.value}
    default_code = 'credentials_error'
