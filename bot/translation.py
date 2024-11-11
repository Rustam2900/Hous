from modeltranslation.translator import TranslationOptions, register
from bot import models


@register(models.User)
class CustomUserTranslation(TranslationOptions):
    fields = ('full_name', 'username', 'state', 'county', 'room')


@register(models.State)
class CustomStateTranslation(TranslationOptions):
    fields = ('name',)


@register(models.County)
class CustomCountyTranslation(TranslationOptions):
    fields = ('name',)


@register(models.House)
class CustomHouseTranslation(TranslationOptions):
    fields = ('title', 'description', 'type', 'room')


@register(models.UserHouseSelection)
class CustomUserHouseSelectionTranslation(TranslationOptions):
    fields = ('user', 'house')
