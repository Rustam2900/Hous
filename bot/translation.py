from modeltranslation.translator import TranslationOptions, register
from bot import models


@register(models.User)
class UserTranslation(TranslationOptions):
    fields = ('full_name', 'username', 'room')


@register(models.State)
class StateTranslation(TranslationOptions):
    fields = ('name',)


@register(models.County)
class CountyTranslation(TranslationOptions):
    fields = ('name',)


@register(models.House)
class HouseTranslation(TranslationOptions):
    fields = ('title', 'description', 'type', 'room')
