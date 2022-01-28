from django.core.management.base import BaseCommand
from brokerage.rest import BrokerEvents

from datetime import datetime
main_id = 'a234caae-b645-4486-876f-306c709e4b4c'
class Command(BaseCommand):
    def handle(self, *args, **options):
        events = BrokerEvents()
        events.stream_all_events()