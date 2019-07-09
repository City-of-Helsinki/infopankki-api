from django.test import TestCase
from info.models import MasterPage


class InfoTestCase(TestCase):
    
    def setUp(self):
        MasterPage.objects.create(meta=dict(one="text", other="text"), page_guid="guid")
    
    def test_master_page(self):
        obj = MasterPage.objects.get(page_guid="guid")
        assert obj.meta['one'] == "text"
