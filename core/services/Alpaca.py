

from alpaca_trade_api.rest import REST
from django.db.models import Sum

class Client:
    base_url ='https://paper-api.alpaca.markets'
    
    def __init__(self,api_key,secret_key,services=None):
        self.rest = REST(api_key,secret_key,self.base_url)
        self.account = self.rest.get_account()
        self.services = services
        
    
    def refresh(self):
        self.account = self.rest.get_account()
        
    @property
    def balance(self):
        return float(self.account.cash)
    @property
    def available_balance(self):
        return self.balance - self.__bot_active_balance()
        
    def __bot_active_balance(self):
        self.locked_balance= self.services.bot_orders.filter(is_active=True).aggregate(total=Sum('investment_amount'))['total']
        return self.locked_balance
    