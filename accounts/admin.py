from django.contrib import admin

from accounts.models import *

admin.site.register(Profile)
admin.site.register(PhotoUser)
admin.site.register(Desk)
admin.site.register(PhotoDesk)
admin.site.register(UserDesk)
admin.site.register(Subscribe)
"""
from django.utils.safestring import mark_safe

from accounts.models import Profile, PhotoUser, PhotoDesk, UserDesk, Desk


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'photo', 'get_photo', 'saved_photo')
    readonly_fields = ('get_photo',)
    search_fields = ('user',)
    autocomplete_fields = ('tags',)
    list_filter = ('tags',)

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src={obj.photo.url} height="80"')
        else:
            return '-'


@admin.register(PhotoUser)
class PhotoUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'photo', 'added')
    sortable_by = ('-added',)
    search_fields = ('user', 'photo')


@admin.register(PhotoDesk)
class PhotoDeskAdmin(admin.ModelAdmin):
    list_display = ('playlist', 'track')


@admin.register(UserDesk)
class UserDeskAdmin(admin.ModelAdmin):
    list_display = ('user', 'playlist', 'added')
    ordering = ('-added',)


@admin.register(Desk)
class DeskAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'published', 'get_image')
    readonly_fields = ('get_image',)
    search_fields = ('^name',)
    autocomplete_fields = ('author', 'photo')
    filter_horizontal = ('photo',)
    list_filter = ('author',)
    sortable_by = ['author', 'name']
    ordering = ('author', 'name',)
    save_on_top = True

    def get_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src={obj.image.url} height="80"')
        else:
            return '-'

    get_image.short_description = "Image" """
