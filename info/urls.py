
from django.conf.urls import url, include
from rest_framework.documentation import include_docs_urls
from rest_framework import routers
from .api import PageViewSet, PageMetaViewSet
from .views import master_view, page_view, translate_view

router = routers.DefaultRouter()
router.register(r'pages', PageViewSet)
router.register(r'meta', PageMetaViewSet)

urlpatterns = [
    url(r'translate/(.*)$', translate_view, name='translate_page'),
    url(r'translations/(.*)$', page_view, name='master_page'),
    url(r'translations$', master_view, name='master_pages'),
    url(r'^docs/', include_docs_urls(title='Infopankki API')),
    url(r'^', include(router.urls)),
]
