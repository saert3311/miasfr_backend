from rest_framework import serializers
from common.serializers import UserDetailSerializer
from .models import Client, Address, Call
from django.db.models import Q

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


class ClientAnonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = [
            'first_name',
            'last_name',
            'main_phone',
            'anon'
        ]

class ClientSerializer(serializers.ModelSerializer):
    user_info = UserDetailSerializer(source="user", read_only=True)
    client_address = AddressSerializer(many=True)

    def create(self, validated_data):
        addresses = validated_data.pop('client_address')
        client_instance = Client.objects.create(**validated_data)
        for address in addresses:
            Address.objects.create(id_client=client_instance, **address)
        return client_instance

    def update(self, instance, validated_data):
        addresses = validated_data.pop('client_address')
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.alternative_email = validated_data.get('alternative_email', instance.alternative_email)
        instance.main_phone = validated_data.get('main_phone', instance.main_phone)
        instance.alternative_phone = validated_data.get('alternative_phone', instance.alternative_phone)
        instance.user = validated_data.get('user', instance.user)
        instance.anon = validated_data.get('anon', instance.anon)
        instance.save()
        for address in addresses:
            Address.objects.create(id_client=instance, **address)
        return instance

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

class ClientBasicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = [
            'id',
            'first_name',
            'last_name',
            'main_phone',
            'alternative_phone',
            'email',
            'alternative_email'
        ]

class CallSerializer(serializers.ModelSerializer):
    callerName = serializers.CharField(read_only=True)
    rawPhone = serializers.CharField(read_only=True)
    is_anon = serializers.BooleanField(read_only=True)

    class Meta:
        model = Call
        fields = '__all__'


class CallClientSerializer(serializers.ModelSerializer):
    client_info = ClientBasicSerializer(source='id_client', read_only=True)

    class Meta:
        model = Call
        fields = '__all__'