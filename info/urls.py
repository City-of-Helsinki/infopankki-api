
from django.conf.urls import url, include
from rest_framework import routers
from .api import PageViewSet
from .views import master_view

router = routers.DefaultRouter()
router.register(r'pages', PageViewSet)

urlpatterns = [
    url(r'translations$', master_view),
    url(r'^', include(router.urls)),
]
