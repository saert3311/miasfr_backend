# Generated by Django 4.0.6 on 2022-07-25 05:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0006_rename_lon_address_lng_remove_client_title_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='user',
        ),
    ]
