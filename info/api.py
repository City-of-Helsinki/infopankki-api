
from info.models import MasterPage, Page
from rest_framework import serializers, viewsets


class PageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Page
        fields = ['language', 'meta', 'created', 'modified', 'url']
        read_only_fields = ['language', 'meta', 'created', 'modified', 'url']


class PageDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ['language', 'meta', 'created', 'modified', 'content']
        read_only_fields = ['language', 'meta', 'created', 'modified', 'url']


class PageViewSet(viewsets.ModelViewSet):

    queryset = Page.objects.all().order_by('modified')

    def get_serializer_class(self):
        if self.action == 'list':
            return PageSerializer
        elif self.action == 'retrieve':
            return PageDetailSerializer
        else:
            return PageSerializer
