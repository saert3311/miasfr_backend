# Generated by Django 4.0.3 on 2022-04-21 02:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='middle_name',
            field=models.CharField(max_length=150, null=True, verbose_name='Middle Name'),
        ),
        migrations.AlterField(
            model_name='client',
            name='suffix',
            field=models.CharField(max_length=15, null=True, verbose_name='Suffix'),
        ),
        migrations.AlterField(
            model_name='client',
            name='title',
            field=models.CharField(max_length=5, null=True, verbose_name='Title'),
        ),
    ]
