from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, 
    PermissionsMixin)
from django.core.validators import MinValueValidator
from core.universe.models import Currency
from core.services.models import BaseTimeStampUidModel

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(("email address"),null=True, blank=True)
    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

class UserBalance(BaseTimeStampUidModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_balance_user_id", db_column="user_id")
    balance = models.FloatField(default=0, validators=[MinValueValidator(0)])
    currency_code = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name="user_balance_currency_code", db_column="currency_code")

    class Meta:
        abstract = True

class UserTransaction(BaseTimeStampUidModel):
    C = "credit"
    D = "debit"
    type_choice = ((C, "credit"), (D, "debit"))
    balance_uid = models.ForeignKey(UserBalance, on_delete=models.CASCADE, related_name="user_transaction_balance_uid", db_column="balance_uid")
    side = models.CharField(max_length=100, choices=type_choice)
    last_balance = models.FloatField(default=0)
    amount = models.FloatField(default=0)
    current_balance = models.FloatField(default=0)
    transaction_detail = models.JSONField(default=dict, null=True, blank=True)
    
    class Meta:
        abstract = True