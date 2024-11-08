from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from bot.models import User, State, County, House, UserHouseSelection


@admin.register(User)
class UserUserAdmin(TranslationAdmin):
    list_display = ('id', 'username', 'phone_number')
    list_display_links = ('id', 'username', 'phone_number')
    search_fields = ('username', 'phone_number')


@admin.register(State)
class StateAdmin(TranslationAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)


@admin.register(County)
class CountyAdmin(TranslationAdmin):
    list_display = ('id', 'name', 'state')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    list_filter = ('state',)


@admin.register(House)
class HouseAdmin(TranslationAdmin):
    list_display = ('id', 'title', 'description', 'price', 'county', 'type', 'created_at')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'description', 'price')
    list_filter = ('type', 'county', 'created_at')


@admin.register(UserHouseSelection)
class UserHouseSelectionAdmin(TranslationAdmin):
    list_display = ('id', 'user', 'house', 'selected_at')
    list_display_links = ('id', 'user', 'house')
    search_fields = ('user__full_name', 'house__title')
    list_filter = ('selected_at', 'user', 'house')
