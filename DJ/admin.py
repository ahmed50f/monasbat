from django.contrib import admin
from .models import DJ
# Register your models here.
@admin.register(DJ)
class DJAdmin(admin.ModelAdmin):
    list_display = ('dj_name', 'price', 'type_event', 'rate', 'created_at')
    list_filter = ('type_event', 'rate')
    search_fields = ('dj_name', 'type_event')
