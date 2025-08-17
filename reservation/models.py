from django.db import models
from hall.models import Hall
from django.conf import settings
# Create your models here.

class Reservation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,  on_delete=models.CASCADE)
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


    


