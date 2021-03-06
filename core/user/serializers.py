from django.contrib.auth import get_user_model, authenticate
from drf_spectacular.utils import (
    OpenApiExample,
    extend_schema_serializer,
)
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers, exceptions
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import (
    TokenObtainSerializer,
    PasswordField,
    api_settings,
    update_last_login,
)
from .models import User
from django.db import IntegrityError

@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "Log in with example account",
            description="Try to log in using an example account",
            value={"email": "ata", "password": "123"},
            request_only=True,
        ),
        OpenApiExample(
            "Example response for user with email 'ata'",
            value={
                "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYyOTUyNTAyOCwianRpIjoiZWQ4NzhjZGQxOGZkNGUyNWIyNjcwNzVjMjk2N2E2NTUiLCJ1c2VybmFtZSI6ImF0YSJ9.oNxgmcsQwEy6MEkKs_7EO5DEjK_QAQGnU15uGOtmo8Y",
                "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjI5NDM5ODI4LCJqdGkiOiIzMWQ0MzUzNDFmNGU0NThiODBiYmMzYzgzZmYxMTc0ZSIsInVzZXJuYW1lIjoiYXRhIn0.8ToPjwJj3ZlQ7mlCsPaV-Fhqq2NV2tyxLeNgi1mk5Nk",
            },
            response_only=True,
        ),
    ],
)
class PairTokenSerializer(TokenObtainSerializer):
    username_field = get_user_model().AUTH_FIELD_NAME

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[self.username_field] = serializers.CharField()
        self.fields["password"] = PasswordField()

    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        authenticate_kwargs = {
            "username": attrs[self.username_field],
            "password": attrs["password"],
        }
        try:
            authenticate_kwargs["request"] = self.context["request"]
        except KeyError:
            pass

        self.user = authenticate(**authenticate_kwargs)

        if not api_settings.USER_AUTHENTICATION_RULE(self.user):
            raise exceptions.AuthenticationFailed(
                self.error_messages["no_active_account"],
                "no_active_account",
            )
        data = {}
        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data


class TokenRevokeSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)
    
    
@extend_schema_serializer(component_name="Accounts Register")

class AccountsRegisterV1Serilaizer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ("email", "password")
        extra_kwargs = {
            "email": {"required": True},
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        try:
            user = User.objects.create_user(**validated_data,is_active=True)
        except IntegrityError as e:
            raise serializers.ValidationError(
                {"email": "User with this email already"}
            )
        except Exception as e:
            raise serializers.ValidationError(
                {"email": str(e)}
            )
        return user
@extend_schema_serializer(component_name="Trade Requirements")

class TradeRequirementsSerializers(serializers.Serializer):
    identity = serializers.BooleanField(read_only=True)
    contact = serializers.BooleanField(read_only=True)
    disclosures = serializers.BooleanField(read_only=True)
    agreement= serializers.BooleanField(read_only=True)
    payment= serializers.BooleanField(read_only=True)

@extend_schema_serializer(component_name="Accounts details")

class UserDetailsV1Serilaizer(serializers.ModelSerializer):
    trade_requirements_status = TradeRequirementsSerializers()
    
    class Meta:
        model = User
        fields = ("email", "trade_requirements_status","trade_status")
        extra_kwargs = {
            'trade_status': {'read_only': True},
            'trade_requirements_status': {'read_only': True}
        }
