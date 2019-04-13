from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Shopkeeper)
admin.site.register(Shop)
admin.site.register(InventoryItem)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Customer)
admin.site.register(Offer)