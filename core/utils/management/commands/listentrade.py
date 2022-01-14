from django.core.management.base import BaseCommand
from core.services.models import Services,BotAction
from core.user.models import User
from core.services.Alpaca import Listener




class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.get(username='admin')
        services:Services = user.services.filter(name='alpaca').get()
        services.login()
        listener = Listener(services.credentials_json['api_key'],services.credentials_json['secret_key'],BotAction)
        listener.run()
        
        