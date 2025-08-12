from django.db import models
from django.contrib.auth.models import User
from hall.models import Hall

# Create your models here.

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.hall.name} on {self.date} from {self.start_time} to {self.end_time}"

    class Meta:
            unique_together = ('hall', 'date', 'start_time', 'end_time')


    


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('visa', 'Visa Card'),
        ('apple_pay', 'Apple Pay'),
        ('cash', 'Cash'),
    ]

    reservation = models.OneToOneField('Reservation', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_data = models.DateTimeField(auto_now_add=True)
    payment_method = payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    card_number = models.CharField(max_length=16, blank=True, null=True)
    card_holder_name = models.CharField(max_length=100, blank=True, null=True)
    card_expiry_date = models.DateField()
    cvv = models.CharField(max_length=3, blank=True, null=True)
