from rest_framework.views import APIView
from rest_framework import response, status, permissions
from .serializers import (
    AccountCredentialsWrapperSerializerv1,
    BankAccountsSerializersV1
    # AccountContactSerializersv1,
    # AccountDetailsSerializersv1,
    # AccountDisclosureSerializersv1,
)
from drf_spectacular.utils import extend_schema
from django.core.exceptions import ObjectDoesNotExist

class AccounUpgradeViewV1(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = AccountCredentialsWrapperSerializerv1

    @extend_schema(
        operation_id="Upgrade account",
    )
    def post(self, request):
        serializers = AccountCredentialsWrapperSerializerv1(data=request.data,context={"request":request})
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return response.Response(
                serializers.data, status=status.HTTP_200_OK
            )
        return response.Response(serializers.error_messages, status=status.HTTP_400_BAD_REQUEST)

class AccountPaymentsViewV1(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = BankAccountsSerializersV1
    
    
    
    @extend_schema(
        operation_id="add Payment Account",
    )
    def post(self, request):
        serializers = BankAccountsSerializersV1(data=request.data)
        
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return response.Response(serializers.data, status=status.HTTP_201_CREATED)
        
        return response.Response(serializers.error_messages, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(
        operation_id="get Payment Account details",
    )
    def get(self,request):
        try:
            bank_acc = request.user.user_bank_account
            serializer = BankAccountsSerializersV1(bank_acc)
            return response.Response(serializer.data,status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return response.Response({'detail':'user doesnt have payment account'},status=status.HTTP_404_NOT_FOUND)
    @extend_schema(
        operation_id="Update Payment Account details",
    )
    def put(self,request):
        try:
            bank_acc = request.user.user_bank_account
            serializer = BankAccountsSerializersV1(bank_acc,data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return response.Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return response.Response({'detail':'user doesnt have payment account'},status=status.HTTP_404_NOT_FOUND)
        
