from django.core.management.base import BaseCommand
from core.services.models import Services
from core.user.models import User
import os

class Command(BaseCommand):
    def handle(self, *args, **options):
        user,created = User.objects.get_or_create(username='admin',email='admin@admin.com',is_staff=True,is_superuser=True)
        if created:
            user.set_password('admin')
            user.save()
            self.stdout.write('User created')
        else:
            self.stdout.write('User exists')
        
            
        services ,service_created= Services.objects.get_or_create(
            name='alpaca',
            credentials_json={"api_key": os.getenv("APC_ID"), "secret_key": os.getenv("APC_SECRET")},
            user = user
            
        )
        if service_created:
            self.stdout.write('Service created')
        else:
            self.stdout.write('Service Exists')
            
        
        