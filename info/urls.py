
from django.conf.urls import url, include
from rest_framework import routers
from .api import PageViewSet

router = routers.DefaultRouter()
router.register(r'pages', PageViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
