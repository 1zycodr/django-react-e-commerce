from django.contrib import admin
from .models import *


class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at',)

admin.site.register(Product)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(Review)
admin.site.register(ShippingAddress)