from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Buyer)
admin.site.register(bank_details)
admin.site.register(verification_details)
admin.site.register(premium_buyer)
admin.site.register(premium_plans)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(notifications)
admin.site.register(saved)