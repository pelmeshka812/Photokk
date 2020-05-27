from django.conf.urls import url
from django.contrib.auth.views import LoginView
from django.urls import path
from django.contrib.auth import views as auth_views

from accounts import views
app_name = 'accounts'
urlpatterns = [

    path('register/', views.register, name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.user_profile, name='user_profile'),
    path('password/reset/done/', views.CustomPasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('password/reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password/confirm/complete/', views.CustomPasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
    path('password/confirm/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('users/', views.user_list, name='user_list'),
    path('users/follow/', views.user_follow, name='user_follow'),
    path('users/<username>/', views.user_detail, name='user_detail'),


]