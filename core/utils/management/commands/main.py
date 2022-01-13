from django.core.management.base import BaseCommand
from core.services.models import Services,BotOrder
from core.user.models import User
class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.get(username='ribonred')
        services:Services = user.services.filter(name='alpaca').get()
        services.login()
        order_bot,created = BotOrder.objects.get_or_create(
            bot_id='CLASSIC_classic_015384',
            investment_amount=1000,
            bot_balance=1000,
            ric='AAPL.O',
            services=services
        )
        # order_bot.get_symbol()
        print(order_bot.get_bot_setup())
        print(services.client.balance)
        print(services.client.available_balance)
        print(services.client.locked_balance)
        