from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings
from django.db.models import Q
from django.core.exceptions import ValidationError

User = settings.AUTH_USER_MODEL

    #Validators functions

def validate_phone(value):
    client_instance = Client.objects.filter(
        Q(main_phone=value) | Q(alternative_phone=value)).exclude(anon=True)
    if client_instance.exists():
        raise ValidationError(f'Phone is registered to {client_instance.first().full_name}')

def validate_email(value):
    client_instance = Client.objects.filter(
        Q(email=value) | Q(alternative_email=value)).exclude(anon=True)
    if client_instance.exists():
        raise ValidationError(f'Email is registered to {client_instance.first().full_name}')

    #And models

class Client(models.Model):
    first_name = models.CharField(max_length=150, verbose_name='First Name')
    last_name = models.CharField(max_length=150, verbose_name='Last Name')
    email = models.EmailField(max_length=100, unique=True, verbose_name='Email', null=True, blank=True, validators=[validate_email])
    alternative_email = models.EmailField(max_length=100, verbose_name='Email', null=True, blank=True, validators=[validate_email])
    main_phone = PhoneNumberField(null=True, unique=True, blank=True, validators=[validate_phone])
    alternative_phone = PhoneNumberField(null=True, blank=True, validators=[validate_phone])
    added = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    anon = models.BooleanField(default=False)

    class Meta:
        ordering = ['-last_name', ]
        indexes = [
            models.Index(fields=['first_name', 'last_name'], name='name_idx'),
            models.Index(fields=['email', 'alternative_email'], name='email_idx'),
            models.Index(fields=['main_phone', 'alternative_phone'], name='phone_idx')
        ]

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def any_phone(self):
        if self.main_phone:
            return str(self.main_phone)
        else:
            return str(self.alternative_phone)

    @property
    def last_call(self):
        return self.client_data.first().date_time

class Address(models.Model):
    TYPE = [
        ('B', 'Billing Address'),
        ('S', 'Shipping Address')
    ]
    id_client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Cliente', related_name='client_address')
    type = models.CharField(max_length=1, choices=TYPE, default='B')
    street = models.CharField(max_length=150, verbose_name='Street')
    city_town = models.CharField(max_length=50, verbose_name='City / Town')
    state_province = models.CharField(max_length=150, verbose_name='State / Province')
    zip = models.CharField(max_length=5, verbose_name='ZIP code')
    country = models.CharField(max_length=50, verbose_name='Country')
    lat = models.DecimalField(max_digits=10, decimal_places=7,  null=True)
    lng = models.DecimalField(max_digits=10, decimal_places=7,  null=True)
    added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id_client.full_name} address'


class Call(models.Model):
    DIRECTIONS = [
        ('I', 'Inbound'),
        ('O', 'Outbound')
    ]
    id_client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='client_data')
    direction = models.CharField(max_length=1, choices=DIRECTIONS, default='I')
    id_user = models.ForeignKey(User, on_delete=models.PROTECT)
    answered = models.BooleanField(default=False)
    date_time = models.DateTimeField()

    def __str__(self):
        return f'{self.id_client.full_name} {self.date_time}'

    @property
    def callerName(self):
        if self.id_client.anon == True:
            return self.id_client.main_phone.as_national
        return self.id_client.full_name

    @property
    def rawPhone(self):
        return self.id_client.main_phone.as_e164

    def is_anon(self):
        return  self.id_client.anon

    def user_name(self):
        return f'{self.id_user.first_name} {self.id_user.last_name}'

    class Meta:
        ordering = ['-date_time']
        get_latest_by = 'date_time'


class MessageTemplate(models.Model):
    message = models.CharField(max_length=160, verbose_name='Message')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']
    def __str__(self):
        splitted = self.message.split()[:4]
        joined = " ".join(splitted)
        return f'{self.pk} - {joined}'

class MessageSent(models.Model):
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name='client_messaged')
    message = models.ForeignKey(MessageTemplate, on_delete=models.PROTECT, related_name='msg_template')
    date_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f'{self.client.first_name} - {self.message.message.split()[:4]}'