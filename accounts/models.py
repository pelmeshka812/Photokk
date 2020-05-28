from django.contrib.auth.models import AbstractUser, User
from django.db import models
from django.urls import reverse
from blog.models import Tag, Photo


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True, default=0)
    tags = models.ManyToManyField(Tag, related_name='users', related_query_name='users', blank=True)
    saved_photo = models.IntegerField(default=0)

    def __str__(self):
        return 'Profile {}'.format(self.user.username)


class PhotoUser(models.Model):
    user = models.ForeignKey(User, related_name='photo',
                             related_query_name='photo', on_delete=models.CASCADE)
    photo = models.ForeignKey(Photo, related_name='owners_photo', default=0, related_query_name='owners_photo',
                              on_delete=models.CASCADE)
    added = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('added',)


class Subscribe(models.Model):
    user_from = models.ForeignKey(User,
                                  related_name='rel_from_set',
                                  related_query_name='rel_from_set',
                                  on_delete=models.CASCADE)
    user_to = models.ForeignKey(User,
                                related_name='rel_to_set',
                                related_query_name='rel_to_set',
                                on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return '{} follows {}'.format(self.user_from, self.user_to)


User.add_to_class('photos',
                  models.ManyToManyField(Photo,
                                         through=PhotoUser,
                                         related_name='owners',
                                         related_query_name='owners',
                                         blank=True, ))

User.add_to_class('following',
                  models.ManyToManyField(User,
                                         through=Subscribe,
                                         related_name='followers',
                                         symmetrical=False))
