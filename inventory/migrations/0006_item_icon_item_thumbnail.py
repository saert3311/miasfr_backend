# Generated by Django 4.0.6 on 2022-08-04 03:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0005_item_user_alter_price_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='icon',
            field=models.ImageField(blank=True, null=True, upload_to='item'),
        ),
        migrations.AddField(
            model_name='item',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='item'),
        ),
    ]
