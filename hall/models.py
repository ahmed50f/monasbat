from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class Hall(models.Model):
    name = models.CharField(max_length=50, verbose_name=_("Hall Name"))
    price = models.PositiveBigIntegerField(verbose_name=_("Price"))
    capacity = models.PositiveIntegerField(verbose_name=_("Capacity"))
    rate = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name=_("Rate (1-5)")
    )
    available_day = models.DateField(null=True, blank=True, verbose_name=_("Available Day"))
    comments = models.TextField(verbose_name=_("Comments"))
    set_the_time = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    extra_Packges = models.ManyToManyField(
        'hall.Extra_Packges', related_name='extra_Packges', blank=True, verbose_name=_("Extra Packages")
    )
    basic_Packges = models.ManyToManyField(
        'hall.Basic_Packges', related_name='basic_Packges', blank=True, verbose_name=_("Basic Packages")
    )
    location = models.CharField(max_length=200, verbose_name=_("Location"))
    image = models.ImageField(upload_to='images/', verbose_name=_("Image"))
    address = models.CharField(max_length=200, verbose_name=_("Address"))
    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))

    class Meta:
        verbose_name = _("Hall")
        verbose_name_plural = _("Halls")

    def __str__(self):
        return self.name


class Extra_Packges(models.Model):
    name = models.CharField(max_length=50, verbose_name=_("Name"))
    price = models.PositiveIntegerField(verbose_name=_("Price"))
    description = models.TextField(verbose_name=_("Description"))
    image = models.ImageField(upload_to='images/', verbose_name=_("Image"))
    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))

    class Meta:
        verbose_name = _("Extra Package")
        verbose_name_plural = _("Extra Packages")

    def __str__(self):
        return self.name


class Basic_Packges(models.Model):
    name = models.CharField(max_length=50, verbose_name=_("Name"))
    price = models.PositiveBigIntegerField(verbose_name=_("Price"))
    description = models.TextField(verbose_name=_("Description"))
    image = models.ImageField(upload_to='images/', verbose_name=_("Image"))
    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))

    class Meta:
        verbose_name = _("Basic Package")
        verbose_name_plural = _("Basic Packages")

    def __str__(self):
        return self.name


class UserHall(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("User Hall Name"))
    contact = models.CharField(max_length=50, verbose_name=_("Contact Info"))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Price"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"))

    class Meta:
        verbose_name = _("User Hall")
        verbose_name_plural = _("User Halls")

    def __str__(self):
        return self.name


