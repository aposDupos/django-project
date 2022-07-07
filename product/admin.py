from django.contrib import admin
from .models import User, Provider, Product, Order

admin.site.register(User)
admin.site.register(Provider)
admin.site.register(Product)
admin.site.register(Order)
