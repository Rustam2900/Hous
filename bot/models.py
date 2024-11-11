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
    state = models.ForeignKey("bot.State", on_delete=models.SET_NULL, null=True, blank=True)
    county = models.ForeignKey("bot.County", on_delete=models.SET_NULL, null=True, blank=True)
    room = models.CharField(_("room"), blank=True, null=True, max_length=50)
    zipcode = models.FloatField(max_length=20, null=True, blank=True)
    min_sum = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    max_sum = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return self.full_name


class State(models.Model):
    name = models.CharField(_("name"), blank=True, max_length=100)

    class Meta:
        verbose_name = _("State")
        verbose_name_plural = _("States")

    def __str__(self):
        return self.name


class County(models.Model):
    name = models.CharField(_("name"), blank=True, max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name="counties")

    class Meta:
        verbose_name = _("County")
        verbose_name_plural = _("Counties")

    def __str__(self):
        return self.name


class House(models.Model):
    class HouseType(models.TextChoices):
        FOR_SALE = 'sale', _("For Sale")
        FOR_RENT = 'rent', _("For Rent")

    title = models.CharField(_("title"), max_length=100, null=True, blank=True)
    description = models.TextField(_("description"), null=True, blank=True)
    zipcode = models.FloatField(null=True, blank=True)
    county = models.ForeignKey(County, on_delete=models.CASCADE, related_name="houses")
    price = models.DecimalField(decimal_places=2, max_digits=10)
    room = models.CharField(_("room"), blank=True, null=True, max_length=50)
    type = models.CharField(
        _("type"), max_length=4, choices=HouseType.choices, default=HouseType.FOR_RENT
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("House")
        verbose_name_plural = _("Houses")

    def __str__(self):
        return f"{self.title} ({self.get_type_display()})"


class UserHouseSelection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="house_selections")
    house = models.ForeignKey(House, on_delete=models.CASCADE, related_name="user_selections")
    selected_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("User House Selection")
        verbose_name_plural = _("User House Selections")

    def __str__(self):
        return f"{self.user.full_name} - {self.house.title}"
