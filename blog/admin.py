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

"""
# Register your models here.
from django.utils.safestring import mark_safe

from account.models import Contact



@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name', '-name')
    prepopulated_fields = {'slug': ('name',)}


class SongsInline(admin.TabularInline):
    model = Song
    extra = 1
    readonly_fields = ('title', 'genre', 'published', 'track', 'image', 'singers')


@admin.register(Singer)
class SingerAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_image')
    readonly_fields = ('get_image',)
    search_fields = ('^name',)
    ordering = ('name',)

    def get_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src={obj.image.url} height="80"')
        else:
            return '-'


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published', 'get_image')
    readonly_fields = ('get_image',)
    list_editable = ('published', 'author')
    search_fields = ('^title',)
    autocomplete_fields = ('author',)
    list_filter = ('author',)
    sortable_by = ['published', 'author', 'title']
    ordering = ('author', '-published', 'title',)
    inlines = [SongsInline]
    save_on_top = True

    def get_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src={obj.image.url} height="80"')
        else:
            return '-'

    get_image.short_description = "Image"


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('title', 'album', 'get_image')
    readonly_fields = ('get_image',)
    search_fields = ('title',)
    autocomplete_fields = ('album', 'singers')
    radio_fields = {'genre': admin.HORIZONTAL}
    list_filter = ['created']
    filter_horizontal = ('singers',)
    sortable_by = ('published', 'title', 'album', 'genre')

    def get_singers(self, obj):
        return "\n".join([s.name for s in obj.singers.all()])

    def get_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src={obj.image.url} height="80"')
        else:
            return '-'

    get_image.short_description = "Image"
    get_singers.short_description = "Singers"


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['user_from', 'user_to', 'created']"""
