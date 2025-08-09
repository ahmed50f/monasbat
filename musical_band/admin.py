from django.contrib import admin
from .models import Musical_Band
# Register your models here.
@admin.register(Musical_Band)
class Musical_BandAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name',)
    ordering = ('name',)