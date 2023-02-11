# Generated by Django 4.1 on 2023-02-08 02:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0012_alter_call_options_alter_call_id_client_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='MessageTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=160, verbose_name='Message')),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='MessageSent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time', models.DateTimeField(auto_now_add=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='client_messaged', to='client.client')),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='msg_template', to='client.messagetemplate')),
            ],
        ),
    ]