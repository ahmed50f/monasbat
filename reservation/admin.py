from django.contrib import admin
from .models import  Reservation, Payment
# Register your models here.
@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display =['user', 'hall', 'date']
    search_fields = ('hall',)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['reservation', 'amount',  'payment_data', 'payment_method']
    search_fields = ('reservation',)
