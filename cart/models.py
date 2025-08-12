# models.py
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()

EVENT_TYPES = [
    ('wedding', 'Wedding'),
    ('birthday', 'Birthday'),
    ('graduation', 'Graduation'),
    ('other', 'Other'),
]

class UserDJ(models.Model):
    STATUS_CHOICES = [('pending', 'pending'), ('approved', 'approved'), ('rejected', 'rejected')]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submitted_djs')
    dj_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    dj_image = models.ImageField(upload_to='user_dj_images', blank=True, null=True)
    available_day = models.DateField(null=True, blank=True)
    set_hour = models.TimeField(null=True, blank=True)
    hall = models.ForeignKey('hall.Hall', on_delete=models.SET_NULL, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    type_event = models.CharField(max_length=50, choices=EVENT_TYPES, blank=True)
    duration = models.DurationField(default=timedelta(hours=1))
    comment = models.TextField(default='No comment', blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.dj_name

class UserMusicalBand(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submitted_bands')
    name = models.CharField(max_length=250)
    band_members = models.CharField(max_length=250, blank=True)
    available_day = models.DateField(null=True, blank=True)
    set_hour = models.TimeField(null=True, blank=True)
    hall = models.ForeignKey('hall.Hall', on_delete=models.SET_NULL, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    comment = models.TextField(default='no comment', blank=True)
    status = models.CharField(max_length=10, choices=UserDJ.STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class UserLight(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submitted_lights')
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    available_day = models.DateField(null=True, blank=True)
    set_hour = models.TimeField(null=True, blank=True)
    hall = models.ForeignKey('hall.Hall', on_delete=models.SET_NULL, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    comment = models.TextField(default='no comment', blank=True)
    status = models.CharField(max_length=10, choices=UserDJ.STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# Cart + CartItem 
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart for {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")

    # الموجود بالفعل فى ال application
    dj = models.ForeignKey('DJ.DJ', on_delete=models.SET_NULL, null=True, blank=True)
    musical_band = models.ForeignKey('musical_band.Musical_Band', on_delete=models.SET_NULL, null=True, blank=True)
    light = models.ForeignKey('lights.Light', on_delete=models.SET_NULL, null=True, blank=True)
    hall = models.ForeignKey('hall.Hall', on_delete=models.SET_NULL, null=True, blank=True)
    

    # دا المستخدم هيضيفه 
    user_dj = models.ForeignKey('DJ.UserDJ', on_delete=models.SET_NULL, null=True, blank=True)
    user_musical_band = models.ForeignKey('musical_band.UserMusical_Band', on_delete=models.SET_NULL, null=True, blank=True)
    user_light = models.ForeignKey('lights.UserLight', on_delete=models.SET_NULL, null=True, blank=True)

    
    added_at = models.DateTimeField(auto_now_add=True)

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
