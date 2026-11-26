from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import UserAccount


@admin.register(UserAccount)
class UserAccountAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (("Extra", {"fields": ("address", "phone", "gender")}),)
    list_display = ("id", "username", "email", "is_staff", "is_active")
