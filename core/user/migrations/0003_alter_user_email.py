# Generated by Django 4.0.1 on 2022-02-06 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_user_trade_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(default=1, max_length=254, unique=True, verbose_name='email address'),
            preserve_default=False,
        ),
    ]
