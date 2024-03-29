from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings
from common.images import make_thumbnail

User = settings.AUTH_USER_MODEL
#signals
from django.dispatch import receiver
from django.db.models.signals import post_save

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Category Name")
    picture = models.ImageField(upload_to='category', null=True, blank=True)
    icon = models.ImageField(upload_to='category', null=True, blank=True)
    thumbnail = models.ImageField(upload_to='category', null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.picture:
            make_thumbnail(self.thumbnail, self.picture, (200, 200), 'thumb')
            make_thumbnail(self.icon, self.picture, (100, 100), 'icon')
        super(Category, self).save(*args, **kwargs)

    @property
    def items_in_category(self):
        return self.item_category.count()

    def __str__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=100, verbose_name="Name")
    description = models.TextField(verbose_name="Description", null=True, blank=True)
    sku = models.CharField(max_length=64, verbose_name="SKU", unique=True)
    active = models.BooleanField(default=True, verbose_name="Item is Active")
    picture = models.ImageField(upload_to='item', null=True, blank=True)
    icon = models.ImageField(upload_to='item', null=True, blank=True)
    thumbnail = models.ImageField(upload_to='item', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="created_by")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name="Category", related_name="item_category")
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        if self.picture:
            make_thumbnail(self.thumbnail, self.picture, (200, 200), 'thumb')
            make_thumbnail(self.icon, self.picture, (100, 100), 'icon')
        super(Item, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    @property
    def current_prices(self):
        return self.item_price.filter(current=True).order_by('period__days')

    @property
    def category_name(self):
        return self.category.name

class Period(models.Model):
    name = models.CharField(max_length=100, verbose_name="Name")
    days = models.IntegerField(default=0, verbose_name="Quantity", unique=True)

    class Meta:
        ordering = ['days']

    def __str__(self):
        return self.name

class Price(models.Model):
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Actual Price")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="price_created_by")
    current = models.BooleanField(default=False, verbose_name="Price is Current")
    item = models.ForeignKey(Item, on_delete=models.PROTECT, verbose_name="Item", related_name="item_price")
    period = models.ForeignKey(Period, on_delete=models.PROTECT, verbose_name="Period Price", related_name="period_price",
                               null=True, blank=True)

    class Meta:
        ordering = ['-updated']

    @property
    def period_days(self):
        return self.period.name

    def clean(self):
        if self.price == 0 or self.price == '':
            raise ValidationError(
                {'Price': "This price is invalid"})

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'${self.price} {self.period.name}'

#after saving new price deactivate old one and making sure only one is active
@receiver(post_save, sender=Price)
def price_created_handler(sender, instance, created, *args, **kwargs):
    if created:
        old_prices = sender.objects.filter(item=instance.item, period=instance.period, current=True).exclude(id=instance.id)
        if old_prices.exists():
            old_prices.update(current=False)
        sender.objects.filter(id=instance.id).update(current=True) #filter and update to not trigger post_save again



class Stock(models.Model):
    quantity = models.IntegerField(default=0, verbose_name="Quantity")
    updated = models.DateTimeField(auto_now_add=True)
    item = models.ForeignKey(Item, on_delete=models.PROTECT, verbose_name="Item Stock", related_name="item_stock")

    class Meta:
        ordering = ['-updated']

    def __str__(self):
        return f'{self.item.name} : {self.quantity}'

class Combo(models.Model):
    name = models.CharField(max_length=50, verbose_name="Name")
    description = models.TextField(verbose_name="Description")
    item = models.ManyToManyField(Item)

    def __str__(self):
        return self.name
