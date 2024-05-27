

# Register your models here.
from django.contrib import admin
from .models import Product, Region, SalesRecord

admin.site.register(Product)
admin.site.register(Region)
admin.site.register(SalesRecord)
