from rest_framework import serializers
from common.serializers import UserDetailSerializer
from .models import Client, Address

class ClientListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = (
            'id',
            'full_name',
            'email',
            'any_phone'
        )

class AddressSerializer(serializers.ModelSerializer):
    id_client = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Address
        fields = '__all__'

class AddressSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

class ClientSerializer(serializers.ModelSerializer):
    user_info = UserDetailSerializer(source="user", read_only=True)
    client_address = AddressSerializer(many=True)

    def create(self, validated_data):
        print(validated_data)
        addresses = validated_data.pop('client_address')
        client_instance = Client.objects.create(**validated_data)
        for address in addresses:
            Address.objects.create(id_client=client_instance, **address)
        return client_instance

    class Meta:
        model = Client
        fields = [
            'first_name',
            'last_name',
            'email',
            'alternative_email',
            'main_phone',
            'alternative_phone',
            'client_address',
            'user_info'
        ]




