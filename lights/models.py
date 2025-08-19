from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from datetime import timedelta
from django.utils.translation import gettext_lazy as _


class Light(models.Model):
    EVENT_TYPES = [
        ('wedding', _("Wedding")),
        ('company_party', _("Company Party")),
        ('private_party', _("Private Party")),
        ('other', _("Other")),
    ]

    hall = models.ForeignKey('hall.Hall', on_delete=models.CASCADE, verbose_name=_("Hall"))
    available_day = models.DateField(null=True, blank=True, verbose_name=_("Available Day"))
    set_hour = models.TimeField(null=True, blank=True, verbose_name=_("Set Hour"))
    event_type = models.CharField(max_length=100, choices=EVENT_TYPES, verbose_name=_("Event Type"))
    duration = models.DurationField(default=timedelta(hours=1), verbose_name=_("Duration"))
    rate = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True,
        blank=True,
        verbose_name=_("Rate (1-5)")
    )
    comments = models.TextField(max_length=500, verbose_name=_("Comments"))
    created_at = models.DateTimeField(default=timezone.now, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("Light")
        verbose_name_plural = _("Lights")

    def __str__(self):
        return f"{self.event_type} - {self.hall.name}"


class UserLight(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    contact = models.CharField(max_length=50, verbose_name=_("Contact Info"))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Price"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"))

    class Meta:
        verbose_name = _("User Light")
        verbose_name_plural = _("User Lights")

    def __str__(self):
        return self.name
