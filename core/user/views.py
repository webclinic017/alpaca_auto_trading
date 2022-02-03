from rest_framework.views import APIView
from rest_framework import response, status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse

from core.user.models import User
from core.utils import api_utils
from .serializers import (
    PairTokenSerializer,
    TokenRevokeSerializer,
)

from .serializers import (
    AccountsRegisterV1Serilaizer,
    AccountDetailsV1Serilaizer
)


class PairTokenView(TokenObtainPairView):
    serializer_class = PairTokenSerializer

    @extend_schema(
        examples=[
            OpenApiExample(
                "detail",
                {
                    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYyOTUyNTAyOCwianRpIjoiZWQ4NzhjZGQxOGZkNGUyNWIyNjcwNzVjMjk2N2E2NTUiLCJ1c2VybmFtZSI6ImF0YSJ9.oNxgmcsQwEy6MEkKs_7EO5DEjK_QAQGnU15uGOtmo8Y",
                    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjI5NDM5ODI4LCJqdGkiOiIzMWQ0MzUzNDFmNGU0NThiODBiYmMzYzgzZmYxMTc0ZSIsInVzZXJuYW1lIjoiYXRhIn0.8ToPjwJj3ZlQ7mlCsPaV-Fhqq2NV2tyxLeNgi1mk5Nk",
                },
                response_only=True,
            )
        ],
        operation_id="Create Token",
    )
    def post(self, request):
        super(PairTokenView, self).post(request)


class RevokeToken(APIView):
    serializer_class = TokenRevokeSerializer

    @extend_schema(
        examples=[
            OpenApiExample("detail", {"detail": "string"}, response_only=True)
        ],
        operation_id="Destroy token",
    )
    def post(self, request):
        """
        revoke token
        """
        serializer = TokenRevokeSerializer(data=request.data)
        if serializer.is_valid():
            try:
                token = RefreshToken(serializer.data["token"])
                token.blacklist()
            except Exception as e:
                return response.Response(
                    {"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST
                )
            return response.Response(
                {"detail": "token revoked"},
                status=status.HTTP_205_RESET_CONTENT,
            )
        return response.Response(
            {"detail": "invalid value"}, status=status.HTTP_400_BAD_REQUEST
        )


class AccountRegisterViewV1(APIView):
    serializer_class = AccountsRegisterV1Serilaizer
    permission_classes = (api_utils.IsPostOrIsAuthenticated,)

    @extend_schema(
        request=AccountsRegisterV1Serilaizer,
        responses={
            201: OpenApiResponse(
                description="Account created successfully",response=api_utils.DefaultMessageSerializer,
            ),
            400: OpenApiResponse(
                description="email is not a valid email address", response=api_utils.DefaultMessageSerializer
            ),
            409: OpenApiResponse(
                description="Account with this email already exists", response=api_utils.DefaultMessageSerializer
            ),
            429: OpenApiResponse(
                description="Too many request", response=api_utils.DefaultMessageSerializer
            )
        },
            examples=[
                OpenApiExample(
                    "Account Registration",
                    description="Try to register an account",
                    value={"email": "ata", "password": "123"},
                    request_only=True,
                ),
                OpenApiExample(
                    "Example success response",
                    value={"detail": api_utils.RegiesterRepsonse.ACCOUNT_CREATED.value},
                    response_only=True,
                    status_codes=[201],
                ),
                OpenApiExample(
                    "Example  email not valid",
                    value={"detail":api_utils.RegiesterRepsonse.EMAIL_NOT_VALID.value},
                    response_only=True,
                    status_codes=[400],
                ),
                OpenApiExample(
                    "Example Account Registration with error syntax email",
                    value={"detail": api_utils.RegiesterRepsonse.ACCOUNT_EXIST.value},
                    response_only=True,
                    status_codes=[409],
                ),
            ],
        operation_id="Create Account",
    )
    def post(self, request):
        serializer = AccountsRegisterV1Serilaizer(User, data=request.data)
        if serializer.is_valid(raise_exception=False):
            serializer.save()
            response = api_utils.DefaultMessageSerializer(
                data={"detail": api_utils.RegiesterRepsonse.ACCOUNT_CREATED.value}
            )
            return response.Response(
                response.data, status=status.HTTP_201_CREATED
            )
    @extend_schema(
        "Account Details",
        responses={
            200: OpenApiResponse(
                description="Account created successfully",response=AccountDetailsV1Serilaizer,
            ),
            401: OpenApiResponse(
                description="permission denied", response=api_utils.DefaultMessageSerializer
            ),
            429: OpenApiResponse(
                description="Too many request", response=api_utils.DefaultMessageSerializer
            )
        }
    )
    def get(self, request):
        serializer = AccountDetailsV1Serilaizer(request.user)
        return response.Response(
                serializer.data, status=status.HTTP_200_OK
            )
    