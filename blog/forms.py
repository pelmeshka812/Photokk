from urllib import request

from django import forms
from django.forms import ModelForm
from blog.models import Photo, Album


class PhotoForm(ModelForm):
    tag = forms.CharField(required=False)

    class Meta:
        model = Photo
        fields = ['photo', 'description', 'name', 'album_id']
        exclude = ('user',)


class AlbumForm(ModelForm):
    class Meta:
        model = Album
        fields = ('name', 'description')
        exclude = ('user',)
