
from info.models import MasterPage, Page, Embed, PageMeta
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
    """
    list:
    Contains metadata and links to individual *Infopankki* page resources
    
    read:
    Page contains metadata and content of individual *Infopankki* page
    """

    queryset = Page.objects.all().order_by('-modified')

    def get_serializer_class(self):
        if self.action == 'list':
            return PageSerializer
        elif self.action == 'retrieve':
            return PageDetailSerializer
        else:
            return PageSerializer


class PageMetaSerializer(serializers.ModelSerializer):

    class Meta:
        model = PageMeta
        fields = ['name', 'url']


class PageUrlSerializer(serializers.ModelSerializer):

    url = serializers.HyperlinkedIdentityField(view_name='page-detail')

    class Meta:
        model = Page
        fields = ['url']


class PageMetaDetailSerializer(serializers.ModelSerializer):

    pages = PageUrlSerializer(read_only=True, many=True)

    class Meta:
        model = PageMeta
        fields = ['name', 'pages']


class PageMetaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    
    list:
    
    
    read:
    
    
    """

    queryset = PageMeta.objects.all().order_by('slug')

    def get_serializer_class(self):
        if self.action == 'list':
            return PageMetaSerializer
        elif self.action == 'retrieve':
            return PageMetaDetailSerializer
        else:
            return PageMetaSerializer
