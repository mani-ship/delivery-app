from django.contrib.auth.models import User
from django.db import models
from .models import * 
from .choice import QUANTITY_CHOICES

from django.db.models.signals import post_save
from django.dispatch import receiver

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.FloatField(default=True)
    discount_price=models.FloatField( default=True)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    country_of_origin = models.CharField(max_length=100,null=True)
    shelf_life = models.CharField(max_length=100,default=True)
    manufacturer_name = models.CharField(max_length=200,default=0)
    manufacturer_address = models.TextField(default=0)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    def __str__(self):
        return self.name


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    quantity_type = models.CharField(max_length=10, choices=QUANTITY_CHOICES,default=True)
    quantity_count = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        multiplier = {
            '250g': 0.25,
            '500g': 0.5,
            '1kg': 1,
            '2kg': 2,
        }
        unit_price = self.product.discount_price or self.product.price
        return unit_price * multiplier[self.quantity_type] * self.quantity_count

    class Meta:
        unique_together = ('user', 'product')

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_approved = models.BooleanField(null=True, blank=True)
    


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    


    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


class Store(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.TextField()
    

# models.py

from django.db import models
from django.contrib.auth.models import User

class UserAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)  
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)  #
    alternate_phone_number = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s address"


class OrderAddressMapping(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE,default=True)
    address = models.ForeignKey(UserAddress, on_delete=models.CASCADE)
    assigned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.order.order_id} -> {self.address}"