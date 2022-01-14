from django.core.management.base import BaseCommand
from core.services.models import Services,BotOrder
from core.user.models import User
class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.get(username='admin')
        services:Services = user.services.filter(name='alpaca').get()
        services.login()
        
        # Creating bot Order
        order_bot:BotOrder; created:bool
        order_bot, created = BotOrder.objects.get_or_create(
            bot_id='CLASSIC_classic_015384',
            investment_amount=1000,
            bot_balance=1000,
            ric='AAPL.O',
            services=services
        )
        # create and save setup
        order_bot.save_setup()
        # actual balance in broker
        print(services.client.balance)
        # balance with used to bot
        print(services.client.available_balance)
        # total of locked balance
        print(services.client.locked_balance)
        
        # submiting order with bot setup
        order_bot.submit_order_with_setup()
        
        
        # services.client.refresh()
        # print(services.client.get_all_orders())
        