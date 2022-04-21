from rest_framework import serializers

from .models import Client, Address

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'main_phone',
            'alternative_phone'
        )