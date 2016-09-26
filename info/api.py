
from info.models import MasterPage, Page
from rest_framework import serializers, viewsets


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page


class PageViewSet(viewsets.ModelViewSet):
    queryset = Page.objects.all().order_by('modified')
    serializer_class = PageSerializer
