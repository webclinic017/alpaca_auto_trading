from rest_framework.views import APIView
from rest_framework import response, status,permissions
from .serializers import AccountCredentialsWrapperSerializerv1

class AccounUpgradeViewV1(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    
    def post(self, request):
        serializers = AccountCredentialsWrapperSerializerv1(data=request.data)
        
        if serializers.is_valid():
            serializers.save()
            return response.Response(serializers.data, status=status.HTTP_200_OK)
        
