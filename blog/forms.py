from urllib import request

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.core.files.base import ContentFile
from django.forms import ModelForm
from django.utils.text import slugify

from blog.models import Photo, Album


class PhotoCreateForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('name', 'url', 'description', )
        widgets = {'url': forms.HiddenInput, }

        def clean_url(self):
            url = self.cleaned_data['url']
            valid_extensions = ['jpg', 'jpeg']
            extension = url.rsplit('_', 1)[1].lower()
            if extension not in valid_extensions:
                raise forms.ValidationError('The given URL does not match valid image extensions')
            return url

        def save(self, force_insert=False, force_update=False, commit=True):
            photo = super(PhotoCreateForm, self).save(commit=False)
            photo_url = self.cleaned_data['url']
            photo_name = '{}.{}'.format(slugify(photo.name), photo_url.rsplit('.', 1)[1].lower())
            response = request.urlopen(photo_url)
            photo.photo.save(photo_name, ContentFile(response.read()),save=False)


class PhotoForm(ModelForm):
    tag = forms.CharField(required=False)

    class Meta:
        model = Photo
        fields = ['photo', 'description', 'name', 'album_id']
        exclude = ('user', )


class AlbumForm(ModelForm):
    class Meta:
        model = Album
        fields = ('name', 'description')
        exclude = ('user', )