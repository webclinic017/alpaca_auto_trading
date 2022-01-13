from django.contrib.auth.models import User, Group
from django.http import HttpResponseRedirect
from rest_framework import views, viewsets, permissions, authentication
from rest_framework.response import Response
from rest_framework_simplejwt import authentication as jwt_authentication
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from .serializers import UserSerializer, GroupSerializer
from .types import LoggedAPIView

_SchemaView = get_schema_view(
   openapi.Info(
      title="App API",
      default_version='v1',
      description="App API",
      contact=openapi.Contact(email="cs@asklora.ai"),
   ),
   # Comment the following line if the API documentation is open to public
   authentication_classes=(authentication.SessionAuthentication,),
   # Comment the following line if the API documentation is open to public
   permission_classes=(permissions.IsAuthenticated,),
)

class SchemaView(_SchemaView):
    def handle_exception(self, exc):
        return HttpResponseRedirect('/login/')

class SampleAPI1(LoggedAPIView, views.APIView):
    # Specify JWT authentication is the only authentication method allowed
    # and the APIView is only accessible if a user sends a request with an
    # access token.
    authentication_classes = [jwt_authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        return Response([{'a': 'SampleAPI1'}])

class UserViewSet(LoggedAPIView, viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

    # Specify JWT authentication is the only authentication method allowed
    # and the APIViewSet is only accessible if a user sends a request with
    # an access token.
    authentication_classes = [jwt_authentication.JWTAuthentication]
    permission_classes = [permissions.IsAdminUser, permissions.IsAuthenticated]

class GroupViewSet(LoggedAPIView, viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    authentication_classes = [jwt_authentication.JWTAuthentication]
    permission_classes = [permissions.IsAdminUser, permissions.IsAuthenticated]