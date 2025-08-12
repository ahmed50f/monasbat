from django.contrib import admin
from .models import Hall, Basic_Packges, Extra_Packges, UserHall
# Register your models here.
@admin.register(Hall)
class HallAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'capacity', 'rate']
    search_fields = ('name', 'address', 'phone', 'email')
    ordering = ('name',)

@admin.register(Basic_Packges)
class Basic_PackagesAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description', 'image', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    ordering = ('name',)

@admin.register(Extra_Packges)  
class Extra_PackgesAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description', 'image', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    ordering = ('name',)

@admin.register(UserHall)
class UserHallAdmin(admin.ModelAdmin):
      list_display = ('name', 'contact', 'price')
      search_fields = ('name', 'contact')      
      list_filter = ('price',)      
      ordering = ('name',) 