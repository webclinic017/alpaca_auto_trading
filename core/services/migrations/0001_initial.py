# Generated by Django 4.0 on 2022-01-13 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Services',
            fields=[
                ('created', models.DateTimeField()),
                ('updated', models.DateTimeField(editable=False)),
                ('uid', models.CharField(editable=False, max_length=255, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('credentials_json', models.JSONField(default=dict)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
