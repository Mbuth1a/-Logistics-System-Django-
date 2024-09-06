from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import*
from django import forms

# Register your models here.
from .models import Driver, Vehicle, CoDriver, Product, Product

admin.site.register(Driver)
admin.site.register(CoDriver)
admin.site.register(Vehicle)
admin.site.register(Product)



