from django.conf import settings
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser, User


class Album(models.Model):
    name = models.CharField(max_length=254, verbose_name='Album name')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_albums')
    description = models.TextField(max_length=500)
    published = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Albums'
        ordering = ['-published']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:album-detail', kwargs={'id': self.id})


class Tag(models.Model):
    tag = models.CharField(max_length=100, verbose_name='Tag name', unique=True)

    class Meta:
        verbose_name_plural = 'Tags'
        ordering = ('tag',)

    def __str__(self):
        return self.name


class Photo(models.Model):
    name = models.CharField(max_length=75, db_index=True)
    user = models.ForeignKey(User, related_name='photo_created', default=0, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="images/", null=True, blank=True)
    url = models.URLField(default=0)
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=200, blank=True)
    album_id = models.ForeignKey(Album, on_delete=models.SET_NULL, null=True, blank=True, related_name='photos',
                                 related_query_name='photos')
    tag = models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True,
                            blank=True, related_name='photos',
                            related_query_name='photos'
                            )
    published = models.DateField(null=True, blank=True, auto_now_add=True)
    users_like = models.ManyToManyField('auth.User',
                                        through='Like',
                                        related_name='images_liked',
                                        blank=True)

    class Meta:
        verbose_name_plural = 'Photos'
        ordering = ['-published']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'id': self.id})


class Like(models.Model):
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='likes_on_photo')

    class Meta:
        unique_together = (('photo', 'user'),)

    def __str__(self):
        return self.photo.name + ': ' + self.user.username


class Dislike(models.Model):
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='dislikes')
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='dislikes_on_photo')

    class Meta:
        unique_together = (('photo', 'user'),)

    def __str__(self):
        return self.photo.name + ': ' + self.user.username


