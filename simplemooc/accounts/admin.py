from django.contrib import admin

from .models import User


class AdminUser(admin.ModelAdmin):
    readonly_fields = ['password']
    list_display = ['username', 'name', 'email', 'is_active']
    search_fields = ['name', 'username', 'email']


admin.site.register(User, AdminUser)
