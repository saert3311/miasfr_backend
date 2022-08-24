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

class ClientSerializer(serializers.ModelSerializer):
    user_info = UserDetailSerializer(source="user", read_only=True)
    client_address = AddressSerializer(many=True)

    #its not cute but it works
    def validate(self, data):
        client_instance_main_phone = Client.objects.filter(Q(main_phone=data['main_phone']) | Q(alternative_phone=data['main_phone']))\
                .exclude(main_phone='')
        if client_instance_main_phone.exists():
            raise serializers.ValidationError(f'Main phone is already registered to {client_instance_main_phone.first().full_name}')

        client_instance_alt_phone = Client.objects.filter(Q(main_phone=data['alternative_phone']) | Q(alternative_phone=data['alternative_phone']))\
                .exclude(alternative_phone='')
        if client_instance_alt_phone.exists():
            raise serializers.ValidationError(f'Alternative phone is already registered to {client_instance_alt_phone.first().full_name}')

        client_instance_email = Client.objects.filter(Q(email=data['email']) | Q(alternative_email=data['email']))\
                .exclude(email__isnull=True)
        if client_instance_email.exists():
            raise serializers.ValidationError(f'Email is already registered {client_instance_email.first().full_name}')

        client_instance_alt_email = Client.objects.filter(Q(email=data['alternative_email']) | Q(alternative_email=data['alternative_email']))\
                .exclude(alternative_email__isnull=True)
        if client_instance_alt_email.exists():
            raise serializers.ValidationError(f'Alternative Email is already registered {client_instance_email.first().full_name}')
        return data


    def create(self, validated_data):
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

class ClientBasicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = [
            'id',
            'first_name',
            'last_name',
            'main_phone',
            'alternative_phone',
            'email'
        ]

class CallSerializer(serializers.ModelSerializer):

    class Meta:
        model = Call
        fields = '__all__'



