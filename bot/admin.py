from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from bot.models import User, State, County, House, HouseImage


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


class HouseImageInline(admin.TabularInline):
    model = HouseImage
    extra = 3
    max_num = 5
    fields = ['image']


@admin.register(House)
class HouseAdmin(TranslationAdmin):
    list_display = ('id', 'title', 'description', 'price', 'county', 'type', 'created_at')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'description', 'price')
    list_filter = ('type', 'county', 'created_at')
    inlines = [HouseImageInline]


