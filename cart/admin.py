from django.contrib import admin
from .models import Cart, CartItem

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    search_fields = ('user__username',)
    list_filter = ('created_at',)


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = (
        'cart',
        'dj',
        'musical_band',
        'light',
        'hall',
        'user_dj',
        'user_musical_band',
        'user_light',
        'added_at',
    )
    search_fields = (
        'cart__user__username',
        'dj__name',
        'musical_band__name',
        'light__name',
        'hall__name',
        'reservation__id',
        'user_dj__dj_name',
        'user_musical_band__name',
        'user_light__name',
    )
    list_filter = ('added_at',)
