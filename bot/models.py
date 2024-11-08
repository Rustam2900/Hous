from django.db import models
from django.utils.translation import gettext_lazy as _
from bot.validators import phone_number_validator

class User(models.Model):
    full_name = models.CharField(_("full name"), blank=True, max_length=255)
    username = models.CharField(_("username"), blank=True, max_length=255, null=True)
    phone_number = models.CharField(blank=True, unique=True, validators=[phone_number_validator],
                                    max_length=20)
    user_lang = models.CharField(blank=True, null=True, max_length=10)
    telegram_id = models.CharField(blank=True, null=True, max_length=255, unique=True)
    tg_username = models.CharField(_("telegram username"), blank=True, null=True, max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    state = models.CharField(_("state"), blank=True, null=True, max_length=100)
    county = models.CharField(_("county"), blank=True, null=True, max_length=100)
    room = models.CharField(_("room"), blank=True, null=True, max_length=50)
    min_sum = models.DecimalField(decimal_places=2, max_digits=10)
    max_sum = models.DecimalField(decimal_places=2, max_digits=10)

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return self.full_name
