from django.core.management.base import BaseCommand
from core.services.models import Services,BotOrder,BotAction
from core.user.models import User
class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.get(username='admin')
        services:Services = user.services.filter(name='alpaca').get()
        services.login()
        # print(services.client.rest.get_last_quote('NCLH'))
        # print(services.client.get_all_positions())
        # action =BotAction.objects.get(pk='f95098efc8e5467cb3c45947ac19ada2')
        # print(action.get_order_details())
        # Creating bot Order
        order_bot:BotOrder; created:bool
        order_bot, created = BotOrder.objects.get_or_create(
            bot_id='CLASSIC_classic_015384',
            investment_amount=15000,
            ric='ALK',
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
        
        
        services.client.refresh()
        print(services.client.get_all_orders())
        