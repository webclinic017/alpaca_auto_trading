from django.db import models
from core.utils import model_enum
from core.utils.models import BaseTimeStampModel, TimestampWithUid
from core.user.models import User


class UserDetails(BaseTimeStampModel):
    user = models.OneToOneField(
        User, on_delete=models.DO_NOTHING, related_name="user_detail_info"
    )
    given_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255)
    family_name = models.CharField(max_length=255)
    date_of_birth = models.CharField(max_length=255)
    tax_id = models.CharField(max_length=255)
    tax_id_type = models.CharField(
        max_length=255,
        choices=model_enum.TaxIdType.choices,
        default=model_enum.TaxIdType.USA_SSN,
    )
    country_of_citizenship = models.CharField(max_length=255)
    country_of_birth = models.CharField(max_length=255)
    country_of_tax_residence = models.CharField(max_length=255)
    funding_source = models.CharField(
        max_length=255, choices=model_enum.FundingSource.choices
    )

    def __str__(self):
        return self.user.email
    
    def dict_fields(self):
        dict_data = dict(
            given_name=self.given_name,
            middle_name=self.middle_name,
            family_name=self.family_name,
            date_of_birth=str(self.date_of_birth),
            tax_id=self.tax_id,
            tax_id_type=self.tax_id_type,
            country_of_citizenship=self.country_of_citizenship,
            country_of_birth=self.country_of_birth,
            country_of_tax_residence=self.country_of_tax_residence,
            funding_source=[self.funding_source]
        )
        return dict_data


class ContactInfo(BaseTimeStampModel):
    user = models.OneToOneField(
        User, on_delete=models.DO_NOTHING, related_name="user_contact_info"
    )
    email_address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    unit = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=255)
    country = models.CharField(max_length=255)

    def __str__(self):
        return self.user.email
    
    def dict_fields(self):
        dic_data = dict(
            email_address=self.email_address,
            phone_number=self.phone_number,
            street_address=[self.street_address],
            city=self.city,
            unit=self.unit,
            state=self.state,
            postal_code=self.postal_code,
            country=self.country
        )
        return dic_data


class Disclosures(BaseTimeStampModel):
    user = models.OneToOneField(
        User, on_delete=models.DO_NOTHING, related_name="user_disclosures_info"
    )
    is_control_person = models.BooleanField(default=False)
    is_affiliated_exchange_or_finra = models.BooleanField(default=False)
    is_politically_exposed = models.BooleanField(default=False)
    immediate_family_exposed = models.BooleanField(default=False)
    employment_status=models.CharField(max_length=255,choices=model_enum.Employment.choices)
    employer_name=models.CharField(max_length=255,null=True,blank=True)		
    employer_address=models.CharField(max_length=255,null=True,blank=True)		
    employment_position=models.CharField(max_length=255,null=True,blank=True)	

    def __str__(self):
        return self.user.email
    
    def dict_fields(self):
        dic_data = dict(
            is_control_person=self.is_control_person,
            is_affiliated_exchange_or_finra=self.is_affiliated_exchange_or_finra,
            is_politically_exposed=self.is_politically_exposed,
            immediate_family_exposed=self.immediate_family_exposed,
            employment_status=self.employment_status,
            employer_name=self.employer_name,
            employer_address=self.employer_address,
            employment_position=self.employment_position
        )
        return dic_data

class Agreements(BaseTimeStampModel):
    agreement = models.CharField(
        max_length=50, choices=model_enum.Agreement.choices
    )
    signed_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.CharField(max_length=50)
    user = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name="user_agreements_info"
    )
    def __str__(self):
        return self.user.email
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "agreement"], name="unique_agreement_user"
            )
        ]


class TrustedContact(BaseTimeStampModel):
    given_name = models.CharField(max_length=255)
    family_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone = models.EmailField(max_length=255)
    user = models.OneToOneField(
        User,
        on_delete=models.DO_NOTHING,
        related_name="user_trusted_contact_info",
    )

    def __str__(self):
        return self.user.email

class Documents(BaseTimeStampModel):
    user = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name="user_documents_info"
    )
    document_type = models.CharField(
        max_length=255, choices=model_enum.DocumentType.choices
    )
    sub_type_document = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField()
    mime_type = models.CharField(max_length=255)

    def __str__(self):
        return self.user.email

    
    constraints = [
            models.UniqueConstraint(
                fields=["user", "document_type"], name="unique_document_user"
            )
        ]
    
    
    
class TradingAccounts(TimestampWithUid):
    user = models.OneToOneField(
        User, on_delete=models.DO_NOTHING, related_name="user_trading_account"
    )
    trading_account_id = models.CharField(max_length=400, blank=True, null=True)
    current_status = models.CharField(
        max_length=255, choices=model_enum.AccountStatus.choices
    )

class BankAccounts(TimestampWithUid):
    user=user = models.OneToOneField(
        User, on_delete=models.DO_NOTHING, related_name="user_bank_account"
    )
    name=models.CharField(max_length=255)
    status=models.CharField(max_length=255,default="QUEUED")
    country=models.CharField(max_length=255,null=True,blank=True)
    state_province=models.CharField(max_length=255,null=True,blank=True)
    postal_code=models.CharField(max_length=255,null=True,blank=True)
    city=models.CharField(max_length=255,null=True,blank=True)
    street_address=models.CharField(max_length=255,null=True,blank=True)
    account_number=models.CharField(max_length=255)
    bank_code=models.CharField(max_length=255)
    bank_code_type=models.CharField(max_length=255,choices=model_enum.BankType.choices,null=True,blank=True)
    is_active=models.BooleanField(default=True)
    
    def __str__(self):
        return self.user.email
    