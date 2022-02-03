
from drf_spectacular.contrib.rest_framework_simplejwt import SimpleJWTScheme

from .token_handler import AuthJwt


class SimpleJWTTokenUserScheme(SimpleJWTScheme):
    name = "jwt_auth"
    target_class = AuthJwt