from modeltranslation.translator import TranslationOptions, register
from bot import models


@register(models.User)
class CustomUserTranslation(TranslationOptions):
    fields = ('full_name', 'username', 'state', 'county', 'room')
