from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from django.utils.translation import gettext_lazy as _   

user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

User = get_user_model()

EVENT_TYPES = [
    ('wedding', _('Wedding')),
    ('birthday', _('Birthday')),
    ('graduation', _('Graduation')),
    ('other', _('Other')),
]

class UserDJ(models.Model):
    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('approved', _('Approved')),
        ('rejected', _('Rejected')),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_("User"))
    dj_name = models.CharField(max_length=100, verbose_name=_("DJ Name"))
    description = models.TextField(blank=True, verbose_name=_("Description"))
    dj_image = models.ImageField(upload_to='user_dj_images', blank=True, null=True, verbose_name=_("DJ Image"))
    available_day = models.DateField(null=True, blank=True, verbose_name=_("Available Day"))
    set_hour = models.TimeField(null=True, blank=True, verbose_name=_("Set Hour"))
    hall = models.ForeignKey('hall.Hall', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Hall"))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Price"))
    type_event = models.CharField(max_length=50, choices=EVENT_TYPES, blank=True, verbose_name=_("Event Type"))
    duration = models.DurationField(default=timedelta(hours=1), verbose_name=_("Duration"))
    comment = models.TextField(default=_('No comment'), blank=True, verbose_name=_("Comment"))
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', verbose_name=_("Status"))
    created_at = models.DateTimeField(default=timezone.now, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    def __str__(self):
        return self.dj_name


class UserMusicalBand(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submitted_bands', verbose_name=_("User"))
    name = models.CharField(max_length=250, verbose_name=_("Band Name"))
    band_members = models.CharField(max_length=250, blank=True, verbose_name=_("Band Members"))
    available_day = models.DateField(null=True, blank=True, verbose_name=_("Available Day"))
    set_hour = models.TimeField(null=True, blank=True, verbose_name=_("Set Hour"))
    hall = models.ForeignKey('hall.Hall', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Hall"))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Price"))
    comment = models.TextField(default=_('No comment'), blank=True, verbose_name=_("Comment"))
    status = models.CharField(max_length=10, choices=UserDJ.STATUS_CHOICES, default='pending', verbose_name=_("Status"))
    created_at = models.DateTimeField(default=timezone.now, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    def __str__(self):
        return self.name


class UserLight(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submitted_lights', verbose_name=_("User"))
    name = models.CharField(max_length=150, verbose_name=_("Light Name"))
    description = models.TextField(blank=True, verbose_name=_("Description"))
    available_day = models.DateField(null=True, blank=True, verbose_name=_("Available Day"))
    set_hour = models.TimeField(null=True, blank=True, verbose_name=_("Set Hour"))
    hall = models.ForeignKey('hall.Hall', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Hall"))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Price"))
    comment = models.TextField(default=_('No comment'), blank=True, verbose_name=_("Comment"))
    status = models.CharField(max_length=10, choices=UserDJ.STATUS_CHOICES, default='pending', verbose_name=_("Status"))
    created_at = models.DateTimeField(default=timezone.now, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    def __str__(self):
        return self.name


# Cart + CartItem 
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart", verbose_name=_("User"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))

    def __str__(self):
        return f"Cart for {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items", verbose_name=_("Cart"))

    # الموجود بالفعل فى ال application
    dj = models.ForeignKey('DJ.DJ', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("DJ"))
    musical_band = models.ForeignKey('musical_band.Musical_Band', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Musical Band"))
    light = models.ForeignKey('lights.Light', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Light"))
    hall = models.ForeignKey('hall.Hall', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Hall"))
    
    # دا المستخدم هيضيفه 
    user_dj = models.ForeignKey('DJ.UserDJ', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("User DJ"))
    user_musical_band = models.ForeignKey('musical_band.UserMusical_Band', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("User Musical Band"))
    user_light = models.ForeignKey('lights.UserLight', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("User Light"))

    added_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Added At"))

    def __str__(self):
        return str(
            self.dj or 
            self.musical_band or 
            self.light or 
            self.hall or 
            self.reservation or
            self.user_dj or
            self.user_musical_band or
            self.user_light
        )
