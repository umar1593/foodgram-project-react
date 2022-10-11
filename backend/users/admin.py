from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ("pk", "username", "email")
    list_filter = UserAdmin.list_filter + ("email", "username")
    search_fields = ["username", "email"]
    empty_value_display = "-пусто-"
