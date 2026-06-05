from django.contrib import admin
from .models import *


class UserAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(is_superuser=False) 

admin.site.register(User, UserAdmin)
admin.site.register(Farmer)
admin.site.register(Buyer)
admin.site.register(chatroom)
admin.site.register(message)
admin.site.register(bloag)
admin.site.register(crop)
admin.site.register(community_message)
admin.site.register(gov_info)