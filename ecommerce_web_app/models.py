from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Category(models.Model):
    category = models.CharField(max_length=50)
    def __str__(self):
        return self.category


class Item(models.Model):
    img = models.ImageField(upload_to='static/img')
    item = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    disc = models.TextField(max_length=10000)
    qty = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Cart(models.Model):
    user = models.CharField(max_length=20)
    item = models.CharField(max_length=200)

class Order(models.Model):
    user = models.CharField(max_length=20, null=False)
    item = models.CharField(max_length=200, null=False)
    qty = models.IntegerField(null=False)
    totel_price = models.FloatField()
    name = models.CharField(max_length=20, null=False)
    number = models.CharField(max_length=20, null=False)
    email = models.CharField(max_length=20, null=False)
    address = models.CharField(max_length=20, null=False)
    address2 = models.CharField(max_length=20, null=False)
    city = models.CharField(max_length=20, null=False)
    state = models.CharField(max_length=20, null=False)
    pin = models.CharField(max_length=8, null=False)
    
    