from rest_framework.viewsets import ModelViewSet
from blog.models import Photo

from blog.serializers import PhotoSerializer


class APIPhotoViewSet(ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer