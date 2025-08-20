from django.contrib import admin
from .models import User  # Assuming you have a User model in apps.accounts.models

from .models import Notification

admin.site.register(User)  # Assuming you have a User model in apps.accounts.models
# Register your models here.
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'sender', 'type', 'is_read', 'created_at')
    list_filter = ('is_read', 'type', 'created_at')
    search_fields = ('title', 'message', 'user__username', 'sender__username')
    readonly_fields = ('created_at',)
