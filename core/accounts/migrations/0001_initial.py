# Generated by Django 4.0.1 on 2022-02-04 08:50

import core.utils.model_enum
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField()),
                ('updated', models.DateTimeField(editable=False)),
                ('given_name', models.CharField(max_length=255)),
                ('middle_name', models.CharField(max_length=255)),
                ('family_name', models.CharField(max_length=255)),
                ('date_of_birth', models.CharField(max_length=255)),
                ('tax_id', models.CharField(max_length=255)),
                ('tax_id_type', models.CharField(choices=[('USA_SSN', 'USA Social Security Number'), ('ARG_AR_CUIT', 'Argentina CUIT'), ('AUS_TFN', 'Australian Tax File Number'), ('AUS_ABN', 'Australian Business Number'), ('BOL_NIT', 'Bolivia NIT'), ('BRA_CPF', 'Brazil CPF'), ('CHL_RUT', 'Chile RUT'), ('COL_NIT', 'Colombia NIT'), ('CRI_NITE', 'Costa Rica NITE'), ('DEU_TAX_ID', 'Germany Tax ID (Identifikationsnummer)'), ('DOM_RNC', 'Dominican Republic RNC'), ('ECU_RUC', 'Ecuador RUC'), ('FRA_SPI', 'France SPI (Reference Tax Number)'), ('GBR_UTR', 'UK UTR (Unique Taxpayer Reference)'), ('GBR_NINO', 'UK NINO (National Insurance Number)'), ('GTM_NIT', 'Guatemala NIT'), ('HND_RTN', 'Honduras RTN'), ('HUN_TIN', 'Hungary TIN Number'), ('IDN_KTP', 'Indonesia KTP'), ('IND_PAN', 'India PAN Number'), ('ISR_TAX_ID', 'Israel Tax ID (Teudat Zehut)'), ('ITA_TAX_ID', 'Italy Tax ID (Codice Fiscale)'), ('JPN_TAX_ID', 'Japan Tax ID (Koijin Bango)'), ('MEX_RFC', 'Mexico RFC'), ('NIC_RUC', 'Nicaragua RUC'), ('NLD_TIN', 'Netherlands TIN Number'), ('PAN_RUC', 'Panama RUC'), ('PER_RUC', 'Peru RUC'), ('PRY_RUC', 'Paraguay RUC'), ('SGP_NRIC', 'Singapore NRIC'), ('SGP_FIN', 'Singapore FIN'), ('SGP_ASGD', 'Singapore ASGD'), ('SGP_ITR', 'Singapore ITR'), ('SLV_NIT', 'El Salvador NIT'), ('SWE_TAX_ID', 'Sweden Tax ID (Personnummer)'), ('URY_RUT', 'Uruguay RUT'), ('VEN_RIF', 'Venezuela RIF'), ('NOT_SPECIFIED', 'Other Tax IDs')], default=core.utils.model_enum.TaxIdType['USA_SSN'], max_length=255)),
                ('country_of_citizenship', models.CharField(max_length=255)),
                ('country_of_birth', models.CharField(max_length=255)),
                ('country_of_tax_residence', models.CharField(max_length=255)),
                ('funding_source', models.CharField(choices=[('employment_income', 'Employment income'), ('investments', 'Investments'), ('inheritance', 'Inheritance'), ('business_income', 'Business income'), ('savings', 'Savings'), ('family', 'Family')], max_length=255)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_detail_info', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TrustedContact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField()),
                ('updated', models.DateTimeField(editable=False)),
                ('given_name', models.CharField(max_length=255)),
                ('family_name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=255)),
                ('phone', models.EmailField(max_length=255)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_trusted_contact_info', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TradingAccounts',
            fields=[
                ('created', models.DateTimeField()),
                ('updated', models.DateTimeField(editable=False)),
                ('uid', models.CharField(editable=False, max_length=255, primary_key=True, serialize=False)),
                ('trading_account_id', models.CharField(blank=True, max_length=400, null=True)),
                ('current_status', models.CharField(choices=[('SUBMITTED', 'Application has been submitted and in process of review'), ('ACTION_REQUIRED', 'Application requires manual action'), ('EDITED', 'Application was edited (e.g. to match info from uploaded docs). This is a transient status.'), ('APPROVAL_PENDING', 'Initial value. Application approval process is in process'), ('APPROVED', 'Account application has been approved, waiting to be ACTIVE'), ('REJECTED', 'Account application is rejected'), ('ACTIVE', 'Account is fully active. Trading and funding can only be processed if an account is ACTIVE.'), ('DISABLED', 'Account is disabled, comes after ACTIVE'), ('ACCOUNT_CLOSED', 'Account is closed')], max_length=255)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_trading_account', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Documents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField()),
                ('updated', models.DateTimeField(editable=False)),
                ('document_type', models.CharField(choices=[('identity_verification', 'Identity verification'), ('address_verification', 'Address verification'), ('date_of_birth_verification', 'Date of birth verification'), ('tax_id_verification', 'Tax ID verification'), ('account_approval_letter', '407 approval letter'), ('w8ben', 'W-8 BEN tax form')], max_length=255)),
                ('sub_type_document', models.CharField(blank=True, max_length=255, null=True)),
                ('content', models.TextField()),
                ('mime_type', models.CharField(max_length=255)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_documents_info', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Disclosures',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField()),
                ('updated', models.DateTimeField(editable=False)),
                ('is_affiliated_exchange_or_finra', models.BooleanField(default=False)),
                ('is_politically_exposed', models.BooleanField(default=False)),
                ('immediate_family_exposed', models.BooleanField(default=False)),
                ('is_control_person', models.BooleanField(default=False)),
                ('employment_status', models.CharField(choices=[('unemployed', 'Unemployed'), ('employed', 'Employed'), ('student', 'Student'), ('retired', 'Retired')], max_length=255)),
                ('employer_name', models.CharField(blank=True, max_length=255, null=True)),
                ('employer_address', models.CharField(blank=True, max_length=255, null=True)),
                ('employment_position', models.CharField(blank=True, max_length=255, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_disclosures_info', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ContactInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField()),
                ('updated', models.DateTimeField(editable=False)),
                ('phone_number', models.CharField(max_length=255)),
                ('street_address', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('unit', models.CharField(max_length=255)),
                ('state', models.CharField(max_length=255)),
                ('postal_code', models.CharField(max_length=255)),
                ('country', models.CharField(max_length=255)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_contact_info', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BankAccounts',
            fields=[
                ('created', models.DateTimeField()),
                ('updated', models.DateTimeField(editable=False)),
                ('uid', models.CharField(editable=False, max_length=255, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('status', models.CharField(max_length=255)),
                ('country', models.CharField(max_length=255)),
                ('state_province', models.CharField(max_length=255)),
                ('postal_code', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('street_address', models.CharField(max_length=255)),
                ('account_number', models.CharField(max_length=255)),
                ('bank_code', models.CharField(max_length=255)),
                ('bank_code_type', models.CharField(max_length=255)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_bank_account', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Agreements',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField()),
                ('updated', models.DateTimeField(editable=False)),
                ('agrement_type', models.CharField(choices=[('MA', 'margin_agreement'), ('AA', 'account_agreement'), ('CA', 'customer_agreement')], max_length=50)),
                ('signed_at', models.DateTimeField(auto_now_add=True)),
                ('ip_address', models.CharField(max_length=50)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_agreements_info', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
