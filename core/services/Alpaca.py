

from alpaca_trade_api.rest import REST
from alpaca_trade_api.stream import Stream
from django.db.models import Sum
from asgiref.sync import sync_to_async
class Client:
    base_url ='https://paper-api.alpaca.markets'
    
    def __init__(self,api_key,secret_key,services=None):
        self.rest = REST(api_key,secret_key,self.base_url)
        self.account = self.rest.get_account()
        self.services = services
        
    def __bot_active_balance(self):
        self.locked_balance= self.services.bot_orders.filter(is_active=True).aggregate(total=Sum('investment_amount'))['total']
        return self.locked_balance
    
    @property
    def available_balance(self):
        return self.balance - self.__bot_active_balance()
        
    @property
    def balance(self):
        return float(self.account.cash)
    
    @property
    def currency(self):
        return self.account.currency
        
    
    def refresh(self):
        self.account = self.rest.get_account()
        
    def get_all_positions(self):
        return self.rest.list_positions()
    
    def get_all_orders(self):
        return self.rest.list_orders()


class Listener:
    base_url ='https://paper-api.alpaca.markets'
    
    
    def __init__(self,api_key,secret_key,bot_action=None):
        self.streamer = Stream(api_key,secret_key,base_url=self.base_url)
        self.bot_action = bot_action
        
    def get_action(self,order_id):
        action_data = self.bot_action.objects.select_related('from_bot').filter(order_broker_id=order_id)
        if action_data.exists():
            return action_data.latest('created')
        
    def save_model(self,model):
        model.save()
    
    async def on_fill(self,data):
        action = await sync_to_async(self.get_action)(data.order.get('client_order_id'))
        action.status = data.order.get('status')
        await sync_to_async(self.save_model)(action)
    
    async def on_canceled(self,data):
        action = await sync_to_async(self.get_action)(data.order.get('client_order_id'))
        action.status = data.order.get('status')
        await sync_to_async(self.save_model)(action)
        
    async def handler(self,data):
        if hasattr(self,f'on_{data.event}'):
            func = getattr(self,f'on_{data.event}')
            await func(data)
        # print("Reply : ",data.order)
    
    def run(self):
        self.streamer.subscribe_trade_updates(self.handler)
        self.streamer.run()
        