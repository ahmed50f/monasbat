from django.contrib import admin
from .models import Light, UserLight

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

@admin.register(UserLight)
class UserLightAdmin(admin.ModelAdmin):
      list_display = ('name', 'contact', 'price')
      search_fields = ('name', 'contact')      
      list_filter = ('price',)      
      ordering = ('name',) 