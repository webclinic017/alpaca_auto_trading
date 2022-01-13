from core.services.models import BaseTimeStampModel
from django.db import models

class Currency(models.Model):
    currency_code = models.CharField(primary_key=True, max_length=30)
    currency_name = models.CharField(blank=True, null=True, max_length=255)
    is_decimal = models.BooleanField(default=False)
    last_price = models.FloatField(blank=True, null=True)
    last_date = models.DateField(blank=True, null=True)

    class Meta:
        abstract = True

class Universe(BaseTimeStampModel):
    ticker = models.CharField(max_length=255, primary_key=True)
    is_active = models.BooleanField(default=True)
    ticker_name = models.TextField(blank=True, null=True)
    currency_code = models.ForeignKey(Currency, on_delete=models.CASCADE, db_column="currency_code", related_name="universe_currency_code", blank=True, null=True)

    class Meta:
        abstract = True