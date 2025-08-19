from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _  

from datetime import timedelta


class DJ(models.Model):
    EVENT_TYPES = [
        ('wedding', _('Wedding')),
        ('birthday', _('Birthday')),
        ('graduation', _('Graduation')),
        ('other', _('Other')),
    ]

    dj_name = models.CharField(max_length=50, verbose_name=_("DJ Name"))
    description = models.TextField(verbose_name=_("Description"))
    dj_image = models.ImageField(upload_to='dj_images', verbose_name=_("DJ Image"))
    available_day = models.DateField(null=True, blank=True, verbose_name=_("Available Day"))
    set_hour = models.TimeField(verbose_name=_("Set Hour"))
    hall = models.ForeignKey('hall.Hall', on_delete=models.CASCADE, verbose_name=_("Hall"))
    price = models.PositiveBigIntegerField(verbose_name=_("Price"))
    type_event = models.CharField(max_length=100, choices=EVENT_TYPES, verbose_name=_("Event Type"))
    duration = models.DurationField(default=timedelta(hours=1), verbose_name=_("Duration"))
    comment = models.TextField(default=_("No comment"), verbose_name=_("Comment"))
    rate = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True, blank=True,
        verbose_name=_("Rate"),
    )
    created_at = models.DateTimeField(default=timezone.now, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    def __str__(self):
        return self.dj_name

    class Meta:
        verbose_name_plural = _('DJs')


class UserDJ(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    contact = models.CharField(max_length=50, verbose_name=_("Contact"))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Price"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = _('Users')
