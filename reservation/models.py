from django.db import models
from hall.models import Hall
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Reservation(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        verbose_name=_("User")
    )
    hall = models.ForeignKey(
        Hall, 
        on_delete=models.CASCADE,
        verbose_name=_("Hall")
    )
    date = models.DateField(verbose_name=_("Date"))
    start_time = models.TimeField(verbose_name=_("Start Time"))
    end_time = models.TimeField(verbose_name=_("End Time"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    is_confirmed = models.BooleanField(default=False, verbose_name=_("Is Confirmed"))

    def __str__(self):
        return f"{self.user.username} - {self.hall.name} on {self.date} from {self.start_time} to {self.end_time}"

    class Meta:
        verbose_name = _("Reservation")
        verbose_name_plural = _("Reservations")
        constraints = [
            models.UniqueConstraint(
                fields=['hall', 'date', 'start_time', 'end_time'],
                name='unique_reservation_per_hall_time'
            )
        ]

