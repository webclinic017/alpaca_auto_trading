from rest_framework import serializers
from . import models
from core.utils.api_utils import DefaultUserSerializers
from django.db import transaction

class AccountContactSerializersv1(DefaultUserSerializers):
    class Meta:
        model = models.ContactInfo
        fields = "__all__"
    
class AccountDetailsSerializersv1(DefaultUserSerializers):
    class Meta:
        model = models.UserDetails
        fields = "__all__"



class AccountDisclosureSerializersv1(DefaultUserSerializers):
    class Meta:
        model = models.Disclosures
        fields = "__all__"

class AccountAgreementsSerializersv1(DefaultUserSerializers):
    class Meta:
        model = models.Agreements
        fields = "__all__"


class AccountTrustedContactSerializersv1(DefaultUserSerializers):
    class Meta:
        model = models.TrustedContact
        fields = "__all__"

class AccountDocumentSerializersv1(DefaultUserSerializers):
    class Meta:
        model = models.Documents
        fields = "__all__"
        
        
class AccountCredentialsWrapperSerializerv1(serializers.Serializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    contact=AccountContactSerializersv1()
    identity=AccountDetailsSerializersv1()
    disclosures=AccountDisclosureSerializersv1()
    agreements=AccountAgreementsSerializersv1()
    
    
    def create(self, validated_data):
        contact_data = validated_data.pop('contact')
        identity_data = validated_data.pop('identity')
        disclosures_data = validated_data.pop('disclosures')
        agreements_data = validated_data.pop('agreements')
        transaction.set_autocommit(False)
        try:
            models.ContactInfo.objects.create(user=self.user,**contact_data)
            models.UserDetails.objects.create(user=self.user,**identity_data)
            models.Disclosures.objects.create(user=self.user,**disclosures_data)
            models.Agreements.objects.create(user=self.user,**agreements_data)
        except Exception:
            transaction.set_autocommit(False)
        
        transaction.commit()
        
        return self.user
    
    
    
