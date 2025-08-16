# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("phone", "email", "full_name", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active")
    ordering = ("phone",)

    fieldsets = (
        (None, {"fields": ("phone", "email", "full_name", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("phone", "email", "full_name", "password1", "password2", "is_staff", "is_active")}
        ),
    )

    search_fields = ("phone", "email", "full_name")

admin.site.register(CustomUser, CustomUserAdmin)

