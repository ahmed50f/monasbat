from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.
class Musical_Band(models.Model):
    name =models.CharField(max_length=250)
    band_members = models.CharField(max_length=250)
    available_day = models.DateField(null=True, blank=True)
    set_hour = models.DateField()
    hall = models.ForeignKey('hall.Hall', on_delete=models.CASCADE)
    price = models.PositiveBigIntegerField()
    comment = models.TextField(default='no comment')
    rate = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Musical Bands'


    
    