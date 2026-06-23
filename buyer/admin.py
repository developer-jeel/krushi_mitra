from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Buyer)
admin.site.register(bank_details)
admin.site.register(verification_details)
admin.site.register(Cart)
admin.site.register(CartItem)