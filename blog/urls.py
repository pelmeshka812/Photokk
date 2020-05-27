from django.urls import path, re_path
from django.views.generic import TemplateView
from blog import views
from blog.views import *

app_name = 'blog'

urlpatterns = [

    path('photos/', views.image_list, name='photos'),
    path('create/', views.PhotoCreateView.as_view(), name='create'),
    re_path(r'^detail/(?P<id>[0-9]+)/$', views.photo_detail, name='detail'),
    path('like/', views.photo_like, name='like'),
    path('', views.image_list, name='list'),
    path('add/', AddPhoto.as_view(), name='add_image'),
    path('follow/', FollowView.as_view(), name='follow'),
    path('album-create/', AlbumCreateView.as_view(), name='album-create'),
    re_path(r'^album-detail/(?P<id>[0-9]+)/$', AlbumDetailView.as_view(), name='album-detail'),
    path('album-list/', AlbumListView.as_view(), name='album-list')


]
