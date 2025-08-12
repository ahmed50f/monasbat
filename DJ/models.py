from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone   

from datetime import timedelta
# Create your models here.
class DJ(models.Model):
    EVENT_TYPES = [
        ('wedding', 'Wedding'),
        ('birthday', 'Birthday'),
        ('graduation', 'Graduation'),
        ('other', 'Other'),
    ]
    dj_name = models.CharField( max_length=50)
    description = models.TextField()
    dj_image = models.ImageField(upload_to='dj_images')
    available_day = models.DateField(null=True, blank=True)
    set_hour = models.TimeField()
    hall = models.ForeignKey('hall.Hall', on_delete=models.CASCADE)
    price = models.PositiveBigIntegerField()
    type_event = models.CharField(max_length=100, choices=EVENT_TYPES)
    duration = models.DurationField(default=timedelta(hours=1))
    comment = models.TextField(default="No comment")
    rate = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.dj_name
    
    class Meta:
        verbose_name_plural = 'DJs'
    

class UserDJ(models.Model):
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
class Meta:
        verbose_name_plural = 'Users'