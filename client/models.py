from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings

User = settings.AUTH_USER_MODEL
# Create your models here.

class Client(models.Model):
    first_name = models.CharField(max_length=150, verbose_name='First Name')
    last_name = models.CharField(max_length=150, verbose_name='Last Name')
    email = models.EmailField(max_length=100, verbose_name='Email', null=True, blank=True)
    alternative_email = models.EmailField(max_length=100, verbose_name='Email', null=True, blank=True)
    main_phone = PhoneNumberField(null=True, blank=True)
    alternative_phone = PhoneNumberField(null=True, blank=True)
    added = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    class Meta:
        ordering = ['-last_name', ]

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    #acuerdate de agregar validacion para que haya al menos un telefono guardado o email
    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def any_phone(self):
        if self.main_phone:
            return str(self.main_phone)
        else:
            return str(self.alternative_phone)

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
