from django.contrib import admin
from .models import Item, Discount, Country, Order


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'currency', 'add_date')
