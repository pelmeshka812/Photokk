from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter

from blog.api import APIPhotoViewSet
from .yasg import urlpatterns as doc_urls

router = DefaultRouter()
router.register('photos', APIPhotoViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('blog/', include('blog.urls')),
    path('main/', TemplateView.as_view(template_name="blog/main.html")),
    path('api/v1/', include(router.urls)),
]

urlpatterns += doc_urls

urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#handler404 = blog.views.error_404
#handler500 = blog.views.error_500