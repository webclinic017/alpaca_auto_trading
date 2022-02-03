from django.core.management.base import BaseCommand
from ...models import Universe


class Command(BaseCommand):
    def handle(self, *args, **options):
        msft:Universe = Universe.objects.get(ticker='MSFT.O')
        print(msft.ticker_symbol)
        
        