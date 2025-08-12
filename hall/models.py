from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.
class Hall(models.Model):
    name = models.CharField( max_length=50)
    price = models.PositiveBigIntegerField()
    capacity = models.PositiveIntegerField()
    rate = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    available_day = models.DateField(null=True, blank=True)
    comments = models.TextField()
    set_the_time = models.DateTimeField(auto_now_add=True)
    extra_Packges = models.ManyToManyField('hall.Extra_Packges', related_name='extra_Packges', blank=True)
    basic_Packges = models.ManyToManyField('hall.Basic_Packges', related_name='basic_Packges', blank=True)
    location = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images/')
    address = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.name
    
class Extra_Packges(models.Model):
    name = models.CharField(max_length=50)
    price = models.PositiveIntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='images/')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    

class Basic_Packges(models.Model):
    name = models.CharField(max_length=50)
    price = models.PositiveBigIntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='images/')
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.name
    

class UserHall(models.Model):
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
