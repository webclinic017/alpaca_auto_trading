

from alpaca_trade_api.rest import REST
from alpaca_trade_api.stream import Stream
from django.db.models import Sum
from asgiref.sync import sync_to_async
import logging
from django.core.management.color import color_style

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
        return float(self.account.buying_power)
    
    @property
    def currency(self):
        return self.account.currency
        
    
    def refresh(self):
        self.account = self.rest.get_account()
        
    def get_all_positions(self):
        return self.rest.list_positions()
    
    def get_detail_position(self, symbol:str):
        return self.rest.get_position(symbol)
    
    def close_position_symbol(self,symbol:str,qty=None):
        return self.rest.close_position(symbol,qty)

    def get_all_orders(self):
        return self.rest.list_orders()
    
    def user_assets(self,status:str=None):
        return self.rest.list_assets(status)


class Listener:
    base_url ='https://paper-api.alpaca.markets'
    color =color_style(True)
    
    
    def __init__(self,api_key,secret_key,bot_action=None):
        self.streamer = Stream(api_key,secret_key,base_url=self.base_url)
        self.bot_action = bot_action
        
    def get_action(self,order_id):
        action_data = self.bot_action.objects.select_related('from_bot').filter(order_broker_id=order_id)
        if action_data.exists():
            return action_data.latest('created')
        
    def record_callback_from_asset(self,asset_id,data):
        action = self.bot_action.objects.select_related('from_bot').filter(from_bot__asset_id=asset_id).latest('created')
        assset = action.from_bot
        
        self.bot_action.objects.create(
            from_bot=assset,
            order_broker_id=data.order.get('client_order_id'),
            status = data.order.get('status'),
            executed_price = float(data.order.get('filled_avg_price')),
            qty = float(data.order.get('qty')),
            invested=0,
            action=data.order.get('side')
        )
        
    def save_model(self,model):
        model.save()
        
    
    async def on_fill(self,data):
        # called on event fill will update bot action and bot order value
        if data.order.get('side') != 'buy':
            # should create sell action
            logging.warning(f"Clossing asset {data.order.get('asset_id')} is {data.order.get('status')} ..." + self.color.SUCCESS("OK"))
            
            await sync_to_async(self.record_callback_from_asset)(data.order.get('asset_id'),data)
            return
        
        action = await sync_to_async(self.get_action)(data.order.get('client_order_id'))
        action.status = data.order.get('status')
        action.executed_price = float(data.order.get('filled_avg_price'))
        await sync_to_async(self.save_model)(action)
        logging.warning(f"Order {action.order_broker_id} side {data.order.get('side')} is {data.order.get('status')} ..." + self.color.SUCCESS("OK"))

        
    
    async def on_canceled(self,data):
        # called on event canceled and update bot action
        action = await sync_to_async(self.get_action)(data.order.get('client_order_id'))
        action.status = data.order.get('status')
        await sync_to_async(self.save_model)(action)
        logging.warning(f"Order {action.order_broker_id} is {data.order.get('status')} ..." + self.color.SUCCESS("OK"))
        
    async def handler(self,data):
        # Handler must be coroutine
        logging.warning(f"Incoming event ..." + self.color.SUCCESS(f"{data.event}"))
        if hasattr(self,f'on_{data.event}'):
            func = getattr(self,f'on_{data.event}')
            await func(data)
        
    
    def run(self):
        # subcribe to listen order change from alpaca
        self.streamer.subscribe_trade_updates(self.handler)
        logging.warning(f"Connection status ..." + self.color.SUCCESS("OK"))
        logging.warning(f"Listening ..." + self.color.SUCCESS("200"))
        
        self.streamer.run()
        