from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User

# Create your models here.

class Client(models.Model):
    title = models.CharField(max_length=5, verbose_name='Title', null=True, blank=True)
    first_name = models.CharField(max_length=150, verbose_name='First Name')
    middle_name = models.CharField(max_length=150, verbose_name='Middle Name', null=True, blank=True)
    last_name = models.CharField(max_length=150, verbose_name='Last Name')
    suffix = models.CharField(max_length=15, verbose_name='Suffix', null=True, blank=True)
    email = models.EmailField(max_length=100, verbose_name='Email', null=True, blank=True)
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

class Address(models.Model):
    id_client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Cliente')
    street = models.CharField(max_length=150, verbose_name='Street')
    city_town = models.CharField(max_length=50, verbose_name='City / Town')
    state_province = models.CharField(max_length=150, verbose_name='State / Province')
    zip = models.CharField(max_length=5, verbose_name='ZIP code')
    country = models.CharField(max_length=50, verbose_name='Country')
    lat = models.DecimalField(max_digits=9, decimal_places=7,  null=True)
    lon = models.DecimalField(max_digits=9, decimal_places=7,  null=True)
    added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id_client.full_name} address'
