from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class Shopkeeper(models.Model):
    auth_user = models.OneToOneField(User, on_delete= models.DO_NOTHING)

class Customer(models.Model):
    auth_user = models.OneToOneField(User, on_delete= models.DO_NOTHING)

class Shop(models.Model):
    name = models.CharField(max_length = 30)
    shopkeeper = models.OneToOneField(Shopkeeper, on_delete=models.CASCADE)
    contact = models.CharField(max_length=10)
    display_picture = models.ImageField( blank=True, null=True, default=None)
    paytm_qr=models.ImageField()

class InventoryItem(models.Model):
    shop = models.ForeignKey( Shop, on_delete = models.CASCADE )
    item_name = models.CharField( max_length = 25 )
    price = models.FloatField( default = 0.0 )
    availability=models.IntegerField(default = 0 )

class Order(models.Model):
    STATUS_ACCEPTED = "ACCEPTED"
    STATUS_REJECTED = "REJECTED"
    STATUS_WAITING = "WAITING CONFIRMATION"
    STATUS_DELIVERED = "DELIVERED"
    CHOICES_STATUS = ((STATUS_REJECTED,STATUS_REJECTED),(STATUS_ACCEPTED,STATUS_ACCEPTED),(STATUS_WAITING,STATUS_WAITING),(STATUS_DELIVERED,STATUS_DELIVERED),)
    
    customer = models.ForeignKey( Customer, on_delete = models.CASCADE )
    shop = models.ForeignKey( Shop, on_delete = models.CASCADE )
    total_price = models.FloatField(default=0.0)
    status = models.CharField(choices = CHOICES_STATUS, default=STATUS_WAITING, max_length=64)
    transaction_id = models.CharField(max_length=16, default="-")
    datetime = models.DateTimeField(default=datetime.now)

class OrderItem(models.Model):
    order = models.ForeignKey( Order, on_delete = models.CASCADE )
    item = models.ForeignKey( InventoryItem, on_delete = models.CASCADE )
    quantity = models.IntegerField(default=0)

class Offer(models.Model):
    shop=models.ForeignKey(Shop, on_delete=models.CASCADE)
    offer=models.TextField(blank=True)
