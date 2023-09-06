from django.contrib import admin
from .models import  CustomUser, Book, CartItem, Order

# Register your models here.
admin.site.register(Book)
admin.site.register(CartItem)
admin.site.register(CustomUser)
admin.site.register(Order)
