from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.conf import settings
class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError(_('The phone number field must be set'))
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(phone_number, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message=_("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    )
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True, unique=True)
    phone_number = models.CharField(validators=[phone_regex], max_length=17, unique=True)
    image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now, editable=False)
    last_updated = models.DateTimeField(_('last updated'), auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone_number

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        
        indexes = [
            models.Index(fields=['phone_number']),
            models.Index(fields=['email']),
        ]


class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('hall', _('Hall')),
        ('dj', _('DJ')),
        ('band', _('Musical Band')),
        ('light', _('Lighting')),
        ('cart', _('Cart')),
        ('account', _('Accounts')),
        ('general', _('General')),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        verbose_name=_('user')
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        related_name='notifications', 
        on_delete=models.CASCADE, 
        verbose_name=_('sender')
    )
    title = models.CharField(_('title'), max_length=255)
    message = models.TextField(_('message'))
    type = models.CharField(_('type'), max_length=20, choices=NOTIFICATION_TYPES, default='general')
    is_read = models.BooleanField(_('is read'), default=False)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)

    class Meta:
        verbose_name = _('Notification')
        verbose_name_plural = _('Notifications')

    def __str__(self):
        return f"[{self.get_type_display()}] {self.title}"