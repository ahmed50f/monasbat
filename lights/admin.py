from django.contrib import admin
from .models import Light

@admin.register(Light)
class LightAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'hall',
        'available_day',
        'set_hour',
        'event_type',
        'duration',
        'rate',
        'created_at',
        'updated_at',
    )
    list_filter = (
        'event_type',
        'available_day',
        'rate',
        'created_at',
    )
    search_fields = (
        'hall__name',
        'event_type',
        'comments',
    )
    ordering = ('-created_at',)

