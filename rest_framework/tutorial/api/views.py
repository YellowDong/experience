from rest_framework import viewsets, permissions
from api.models import BlogModel, TagModel
from api.serializers import BlogSerializer, TagSerializer


class BlogListView(viewsets.ModelViewSet):
    queryset = BlogModel.objects.all()
    permission_class = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = BlogSerializer


class TagView(viewsets.ModelViewSet):
    queryset = TagModel.objects.all()
    permission_class = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = TagSerializer







