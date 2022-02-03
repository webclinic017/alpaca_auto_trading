from core.utils.models import TimestampWithUid, Universe
from core.utils.modelhelper import updatesetter
from core.user.models import User
from django.db import models
from .Alpaca import Client as AlpacaClient
from DroidRpc.client import Client as Droid
from django.conf import settings
from django.utils import timezone


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
    services:Services = models.ForeignKey(
        Services, on_delete=models.CASCADE, related_name="bot_orders"
    )
    bot_balance = models.FloatField(default=0)
    ric = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    spot_date = models.DateField(null=True, blank=True)
    expiry = models.DateField(null=True, blank=True)
    max_loss_price = models.FloatField(null=True, blank=True,default=0)
    max_loss_amount = models.FloatField(null=True, blank=True,default=0)
    target_profit_pct = models.FloatField(null=True, blank=True,default=0)
    target_profit_price = models.FloatField(null=True, blank=True,default=0)
    target_profit_amount = models.FloatField(null=True, blank=True,default=0)
    is_executed = models.BooleanField(default=False)
    executed_at = models.DateTimeField(null=True, blank=True)
    asset_id = models.CharField(max_length=255, null=True, blank=True)
    asset_type = models.CharField(max_length=255, null=True, blank=True)
    bot_holding_share = models.FloatField(default=0)
    
    droid: Droid = Droid(address=settings.ASKLORA_DROID)

    def save(self, *args, **kwargs):
        if not self.bot_balance:
            self.bot_balance = self.investment_amount
            super(BotOrder, self).save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.bot_id} - {self.services.uid}"

    def get_symbol(self):
        universe:Universe = Universe.objects.get(ticker=self.ric)
        return universe.ticker_symbol

    def get_bot_setup(self, price=None):
        if not price:
            self.services.login()
            prices =self.services.client.rest.get_last_quote(self.get_symbol())
            
            if not prices.askprice:
                prices=self.services.client.rest.get_latest_bar(self.get_symbol())
                price_ = prices.c
            else:
                price_ =prices.askprice
            price = price_
        data = self.droid.create_bot(
            self.ric,
            self.created.date().strftime("%Y-%m-%d"),
            self.investment_amount,
            price,
            self.bot_id,
        )
        return data

    def save_setup(self,price=None):
        setup = self.get_bot_setup(price)
        setup.pop('created')
        model = updatesetter(self,setup)
        model.save()
        
    def amount(self,qty,price):
        return round(qty * price,4)
    
    
    def submit_order_with_setup(self,price=None):
        self.services.login()
        setup = self.get_bot_setup(price)
        take_profit = {
            'limit_price':round(setup.get('target_profit_price'),2)
        }
        stop_loss = {
             'limit_price':round(setup.get('max_loss_price'),2),
             'stop_price':round(setup.get('max_loss_price'),2)
        }
        print(take_profit,stop_loss)
        print("="*8)
        order = self.services.client.rest.submit_order(
            self.get_symbol(),
            setup.get('share_num'),
            setup.get('side').lower(),
            "limit",
            "day",
            limit_price=round(setup.get('entry_price'),2),
            order_class="bracket",
            take_profit=take_profit,
            stop_loss=stop_loss
        )
        amount_invested =round(float(order.qty) * float(order.limit_price),4)
        BotAction.objects.create(
            from_bot=self,
            action=order.side,
            order_broker_id=order.client_order_id,
            invested=amount_invested,
            executed_price=float(order.limit_price),
            status=order.status,
            qty=float(order.qty)
        )
        # self.bot_balance = round(self.bot_balance - amount_invested,4)
        self.asset_id = order.asset_id
        self.asset_type = order.asset_class
        self.is_executed = True
        self.executed_at = timezone.now()
        self.save()

class BotAction(TimestampWithUid):
    from_bot:BotOrder = models.ForeignKey(BotOrder,on_delete=models.CASCADE,related_name="actions")
    action = models.CharField(max_length=255)
    order_broker_id = models.CharField(max_length=255,null=True, blank=True)
    status = models.CharField(max_length=255)
    invested = models.FloatField(default=0)
    executed_price = models.FloatField(default=0)
    qty = models.FloatField(default=0)
    
    def __str__(self):
        return f"{self.from_bot.bot_id} - {self.action}"
     
    def get_order_details(self):
        if not self.order_broker_id:
            return None
        self.from_bot.services.login()
        return self.from_bot.services.client.rest.get_order_by_client_order_id(self.order_broker_id)

    def share_change(self):
        if self.action == 'buy':
            return self.qty
        elif self.action == 'sell':
            return -self.qty
    def save(self, *args, **kwargs):
        if self.status == "filled":
            invest = round(self.qty * self.executed_price,2)
            bot_order:BotOrder = BotOrder.objects.get(pk=self.from_bot.pk)
            if self.action == 'buy':
                self.invested = invest
                invest= -invest
            elif self.action == 'sell':
                invest = invest
                self.invested = 0
                bot_order.is_active = False
            bot_order.bot_balance = round(bot_order.bot_balance + invest,2)
            print("BEFORE",bot_order.bot_holding_share)
            
            bot_order.bot_holding_share = bot_order.bot_holding_share + self.share_change()
            print(bot_order.bot_holding_share)
            bot_order.save()
            super(BotAction, self).save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)
        
