
import uuid
from django.db import models
from django.contrib.postgres.fields import HStoreField
from django_extensions.db.models import TimeStampedModel


class BaseModel(TimeStampedModel):
    """
    Each BaseModel has creation and modification time stamps, a name and one or more tags

    Tags are for lists of arbitrary relations
    """

    class Meta:
        abstract = True

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return "{0}".format(self.name)


class MasterPage(BaseModel):
    meta = HStoreField(blank=True, null=True)
    page_guid = models.CharField("Original page GUID", max_length=50, editable=False)


class Page(BaseModel):
    master = models.ForeignKey(MasterPage)
    language = models.CharField(max_length=3)
    meta = HStoreField(blank=True, null=True)


class Doc(BaseModel):
    page = models.ForeignKey(Page)
    doc_id = models.IntegerField("Original document ID", editable=False)
    content = models.TextField()
