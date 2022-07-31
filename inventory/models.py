from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Category Name")

class Item(models.Model):
    name = models.CharField(max_length=100, verbose_name="Name")
    sku = models.CharField(max_length=64, verbose_name="SKU")
    active = models.BooleanField(default=True, verbose_name="Item is Active")
    picture = models.ImageField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name="Category", related_name="item_category")


    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def current_price(self):
        return self.price.price

class Price(models.Model):
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Actual Price")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="created_by")
    current = models.BooleanField(default=False, verbose_name="Price is Current")
    item = models.ForeignKey(Item, on_delete=models.PROTECT, verbose_name="Item", related_name="item_price")

    class Meta:
        ordering = ['-updated']

    def __str__(self):
        return f'{self.item.name} : {self.price}'

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
