from django.contrib import admin
from .models import Musical_Band, UserMusical_Band
# Register your models here.
@admin.register(Musical_Band)
class Musical_BandAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(UserMusical_Band)
class UserMusical_BandAdmin(admin.ModelAdmin):
      list_display = ('name', 'contact', 'price')
      search_fields = ('name', 'contact')      
      list_filter = ('price',)      
      ordering = ('name',) 