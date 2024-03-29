# Generated by Django 4.1 on 2022-08-16 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0009_call_client_anon_client_name_idx_client_email_idx_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='client',
            name='Unique Email',
        ),
        migrations.RemoveConstraint(
            model_name='client',
            name='Unique Phone',
        ),
        migrations.AddConstraint(
            model_name='client',
            constraint=models.UniqueConstraint(fields=('main_phone', 'alternative_phone'), name='unique_phone'),
        ),
    ]
