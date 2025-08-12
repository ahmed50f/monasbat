from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone   
from datetime import timedelta
# Create your models here.


class Light(models.Model):
    EVENT_TYPES = [
        ('wedding', 'Wedding'),
        ('company_party', 'Company_Party'),
        ('private_party', 'Private_Party'),
        ('other', 'Other'),
    ]
    hall = models.ForeignKey('hall.Hall', on_delete=models.CASCADE)
    available_day = models.DateField(null=True, blank=True)
    set_hour = models.TimeField(null=True, blank=True)
    event_type = models.CharField(max_length=100, choices=EVENT_TYPES)
    duration = models.DurationField(default=timedelta(hours=1))
    rate = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=True, blank=True)
    comments = models.TextField(max_length=500)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return super().__str__()

class UserLight(models.Model):
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    def __str__(self):
        return f"{self.event_type} - {self.hall.name}"


   
