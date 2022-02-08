# Generated by Django 4.0.1 on 2022-02-08 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_remove_agreements_unique_agreement_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankaccounts',
            name='bank_code_type',
            field=models.CharField(blank=True, choices=[('ABA', 'Domestic'), ('BIC', 'International')], max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='bankaccounts',
            name='city',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='bankaccounts',
            name='country',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='bankaccounts',
            name='postal_code',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='bankaccounts',
            name='state_province',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='bankaccounts',
            name='status',
            field=models.CharField(default='QUEUED', max_length=255),
        ),
        migrations.AlterField(
            model_name='bankaccounts',
            name='street_address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
