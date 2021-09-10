from django.contrib import admin

# Register your models here.
from order.models import DiscountCode, Order, OrderHistory

admin.site.register(DiscountCode)

admin.site.register(Order)

admin.site.register(OrderHistory)

