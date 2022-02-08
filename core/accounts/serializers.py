from rest_framework import serializers, exceptions
from core.accounts.broker_accounts import AccountBrokerServices

from core.utils.modelhelper import updatesetter
from . import models
from core.utils.api_utils import DefaultUserSerializers
from django.db import IntegrityError, transaction
from drf_spectacular.utils import extend_schema_serializer,OpenApiExample


@extend_schema_serializer(component_name="Accounts contact info")
class AccountContactSerializersv1(DefaultUserSerializers):
    class Meta:
        model = models.ContactInfo
        exclude = ("created", "updated", "id")


@extend_schema_serializer(component_name="Accounts details")
class AccountDetailsSerializersv1(DefaultUserSerializers):
    class Meta:
        model = models.UserDetails
        exclude = ("created", "updated", "id")


@extend_schema_serializer(component_name="Accounts Disclosures")
class AccountDisclosureSerializersv1(DefaultUserSerializers):
    class Meta:
        model = models.Disclosures
        exclude = ("created", "updated", "id")


@extend_schema_serializer(component_name="Accounts Agreements")
class AccountAgreementsSerializersv1(DefaultUserSerializers):
    class Meta:
        model = models.Agreements
        exclude = ("created", "updated", "id")


class AccountTrustedContactSerializersv1(DefaultUserSerializers):
    class Meta:
        model = models.TrustedContact
        exclude = ("created", "updated", "id")


class AccountDocumentSerializersv1(DefaultUserSerializers):
    class Meta:
        model = models.Documents
        exclude = ("created", "updated", "id")


@extend_schema_serializer(
    component_name="Accounts credentials",
    examples=[
        OpenApiExample(
            "Valid example",
            value={
    "contact": {
        "email_address": "ribonred@hotmail.com",
        "phone_number": "555-666-7788",
        "street_address": "20 N San Mateo Dr",
        "unit": "Apt 1A",
        "city": "San Mateo",
        "state": "CA",
        "postal_code": "94401",
        "country": "USA"
    },
    "identity": {
        "given_name": "Rede",
        "middle_name": "zora",
        "family_name": "widodo",
        "date_of_birth": "1988-08-12",
        "tax_id": "666-55-4321",
        "tax_id_type": "USA_SSN",
        "country_of_citizenship": "USA",
        "country_of_birth": "USA",
        "country_of_tax_residence": "USA",
        "funding_source": "employment_income"
    },
    "disclosures": {
        "is_control_person": False,
        "is_affiliated_exchange_or_finra": False,
        "is_politically_exposed": False,
        "immediate_family_exposed": False,
        "employment_status": "unemployed"
    },
    "agreements": [{
            "agreement": "MA",
            "ip_address": "185.13.21.99"
        },
        {
            "agreement": "AA",
            "ip_address": "185.13.21.99"
        },
        {
            "agreement": "CA",
            "ip_address": "185.13.21.99"
        }
    ]
},
            request_only=True,  # signal that example only applies to requests
            response_only=False,  # signal that example only applies to responses
        ),
    ],
)
class AccountCredentialsWrapperSerializerv1(serializers.Serializer):
    contact = AccountContactSerializersv1()
    identity = AccountDetailsSerializersv1()
    disclosures = AccountDisclosureSerializersv1()
    agreements = AccountAgreementsSerializersv1(many=True)

    def create(self, validated_data):
        contact_data = validated_data.pop("contact")
        identity_data = validated_data.pop("identity")
        disclosures_data = validated_data.pop("disclosures")
        agreements_data = validated_data.pop("agreements")
     
        transaction.set_autocommit(False)
        try:
            contact = models.ContactInfo.objects.create(**contact_data)
        except IntegrityError:
            raise exceptions.ParseError(
                detail=f"contact info already exists,use update instead"
            )
        except Exception as e:
            raise exceptions.APIException(detail=str(e))
        try:
            identity = models.UserDetails.objects.create(**identity_data)
        except IntegrityError:
            raise exceptions.ParseError(
                detail=f"identity info already exists,use update instead"
            )
        except Exception as e:
            raise exceptions.APIException(detail=str(e))
        try:
            disclosure = models.Disclosures.objects.create(**disclosures_data)
        except IntegrityError:
            raise exceptions.ParseError(
                detail=f"disclosure info already exists,use update instead"
            )
        except Exception as e:
            raise exceptions.APIException(detail=str(e))
        for agree_data in agreements_data:
            try:
                agrement = models.Agreements.objects.create(**agree_data)
            except IntegrityError:
                raise exceptions.ParseError(
                    detail=f"Agreement type {agree_data['agreement']} already exists"
                )
            except Exception as e:
                raise exceptions.APIException(detail=str(e))
        
        try:
            brokerage = AccountBrokerServices(contact_data['user'])
            brokerage.activate_account()
        except Exception as e:
            raise exceptions.ParseError(detail=e)

        transaction.commit()

        return {
            "contact": AccountContactSerializersv1(contact).data,
            "identity": AccountDetailsSerializersv1(identity).data,
            "disclosures": AccountDisclosureSerializersv1(disclosure).data,
            "agreements": AccountAgreementsSerializersv1(
                models.Agreements.objects.filter(user=identity.user), many=True
            ).data,
        }
        
@extend_schema_serializer(component_name="Accounts Payments")
class BankAccountsSerializersV1(DefaultUserSerializers):
    class Meta:
        model = models.BankAccounts
        exclude =('created', 'updated')
        extra_kwargs = {
            'is_active':{
                'read_only': True,
            },
            'uid':{
                'read_only':True
            },
            'status':{
                'read_only':True
            },
        }
        
    
    def create(self, validated_data):
        try:
            bank_account =models.BankAccounts.objects.create(**validated_data)
            return bank_account
        except IntegrityError:
            raise exceptions.ParseError('Bank account already exists, please update the existing')
    
    def update(self,instance,validated_data):
        bank = updatesetter(instance,validated_data)
        bank.save()
        return bank
    


class TradingAccountsSerializerV1(DefaultUserSerializers):
    class Meta:
        model =models.TradingAccounts
        fields ='__all__'
        
        
