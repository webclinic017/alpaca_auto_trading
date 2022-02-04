from rest_framework import serializers,permissions,status
from rest_framework.exceptions import APIException

from core.utils.model_enum import AuthorizationEnum


class DefaultUserSerializers(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())



class IsPostOrIsAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        # allow all POST requests
        if request.method == "POST":
            return True

        # Otherwise, only allow authenticated requests
        # Post Django 1.10, 'is_authenticated' is a read-only attribute
        return request.user and request.user.is_authenticated





class DefaultMessageSerializer(serializers.Serializer):
    detail = serializers.CharField()
    

class AuthorizationException(APIException):
    """
    change 401 to 403
    """
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = {'detail': AuthorizationEnum.PERMISSIONS_ERROR.value}
    default_code = 'credentials_error'
