from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _


class Musical_Band(models.Model):
    name = models.CharField(max_length=250, verbose_name=_("Band Name"))
    band_members = models.CharField(max_length=250, verbose_name=_("Band Members"))
    available_day = models.DateField(null=True, blank=True, verbose_name=_("Available Day"))
    set_hour = models.TimeField(verbose_name=_("Set Hour"))  
    hall = models.ForeignKey('hall.Hall', on_delete=models.CASCADE, verbose_name=_("Hall"))
    price = models.PositiveBigIntegerField(verbose_name=_("Price"))
    comment = models.TextField(default=_("No comment"), verbose_name=_("Comment"))
    rate = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True,
        blank=True,
        verbose_name=_("Rate (1-5)")
    )
    created_at = models.DateTimeField(default=timezone.now, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Musical Band")
        verbose_name_plural = _("Musical Bands")


class UserMusical_Band(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    contact = models.CharField(max_length=50, verbose_name=_("Contact Info"))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Price"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("User Musical Band")
        verbose_name_plural = _("User Musical Bands")
