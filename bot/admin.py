from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from bot.models import User

@admin.register(User)
class UserUserAdmin(TranslationAdmin):
    list_display = ('id', 'username', 'phone_number')
    list_display_links = ('id', 'username', 'phone_number')
    search_fields = ('username', 'phone_number')