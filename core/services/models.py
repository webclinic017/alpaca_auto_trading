from core.utils.models import TimestampWithUid
from core.user.models import User
from django.db import models
from .Alpaca import Client as AlpacaClient
from DroidRpc.client import Client as Droid
from django.conf import settings
# Create your models here.

class Services(TimestampWithUid):
    name = models.CharField(max_length=255)
    credentials_json = models.JSONField(default=dict)
    user: User = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="services"
    )
    client: AlpacaClient

    def __str__(self):
        return f"{self.name} - {self.user.username}"

    def login(self):
        self.client = AlpacaClient(
            self.credentials_json["api_key"],
            self.credentials_json["secret_key"],
            services=self,
        )


class BotOrder(TimestampWithUid):
    bot_id = models.CharField(max_length=255)
    investment_amount = models.FloatField()
    services = models.ForeignKey(
        Services, on_delete=models.CASCADE, related_name="bot_orders"
    )
    bot_balance = models.FloatField()
    ric = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    droid: Droid = Droid(address="47.243.56.42")


    def save(self, *args, **kwargs):
        if not self.bot_balance:
            self.bot_balance = self.investment_amount
            super(BotOrder, self).save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.bot_id} - {self.services.uid}"
    
    def get_symbol(self):
        universe = settings.DATASET['universe']
        res = universe.find_one(ticker=self.ric).get('ticker_symbol')
        return res

    def get_bot_setup(self, price=None):
        if not price:
            self.services.login()
            price_ = self.services.client.rest.get_latest_bar(self.get_symbol())
            price = price_.c
        data = self.droid.create_bot(
            self.ric,
            self.created.date().strftime("%Y-%m-%d"),
            self.investment_amount,
            price,
            self.bot_id,
        )
        return data
