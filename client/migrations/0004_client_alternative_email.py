# Generated by Django 4.0.6 on 2022-07-23 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0003_address_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='alternative_email',
            field=models.EmailField(blank=True, max_length=100, null=True, verbose_name='Email'),
        ),
    ]
