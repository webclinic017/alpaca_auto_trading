# Generated by Django 4.0 on 2022-01-13 07:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BotOrder',
            fields=[
                ('created', models.DateTimeField()),
                ('updated', models.DateTimeField(editable=False)),
                ('uid', models.CharField(editable=False, max_length=255, primary_key=True, serialize=False)),
                ('bot_id', models.CharField(max_length=255)),
                ('investment_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('bot_balance', models.DecimalField(decimal_places=2, max_digits=10)),
                ('managed_asset_symbol', models.CharField(max_length=255)),
                ('is_active', models.BooleanField(default=True)),
                ('services', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bot_orders', to='services.services')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
