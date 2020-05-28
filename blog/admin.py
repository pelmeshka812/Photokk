from django.contrib import admin

from blog.models import Photo, Like, Dislike, Album


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'photo', 'published']
    list_filter = ['published']


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('photo', 'user')


@admin.register(Dislike)
class DislikeAdmin(admin.ModelAdmin):
    list_display = ('photo', 'user')


admin.site.register(Album)


