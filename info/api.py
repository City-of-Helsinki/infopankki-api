
from info.models import MasterPage, Page, Embed
from rest_framework import serializers, viewsets

class EmbedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Embed
        fields = ['uri']


class PageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Page
        fields = ['language', 'meta', 'created', 'modified', 'url']
        read_only_fields = ['language', 'meta', 'created', 'modified', 'url']


class PageDetailSerializer(serializers.ModelSerializer):
    embeds = EmbedSerializer(many=True, read_only=True)

    class Meta:
        model = Page
        fields = ['language', 'meta', 'created', 'modified', 'content', 'embeds']
        read_only_fields = ['language', 'meta', 'created', 'modified', 'url']


class PageViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Page.objects.all().order_by('-modified')

    def get_serializer_class(self):
        if self.action == 'list':
            return PageSerializer
        elif self.action == 'retrieve':
            return PageDetailSerializer
        else:
            return PageSerializer
