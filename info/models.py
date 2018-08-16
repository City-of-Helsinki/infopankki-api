
import uuid
from django.db import models
from django.contrib.postgres.fields import HStoreField, ArrayField
from django_extensions.db.models import TimeStampedModel


class BaseModel(TimeStampedModel):
    """
    Each BaseModel has creation and modification time stamps, a name and one or more tags

    Tags are for lists of arbitrary relations
    """

    class Meta:
        abstract = True

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


class MasterPage(BaseModel):
    meta = HStoreField(blank=True, null=True)
    page_guid = models.CharField("Original page GUID", max_length=50, editable=False)

    def __str__(self):
        return str(self.id)

    def __rep__(self):
        return str(self)


class Page(BaseModel):
    master = models.ForeignKey(MasterPage, related_name="pages")
    language = models.CharField(max_length=3)
    meta = HStoreField(blank=True, null=True)
    doc_title = models.TextField(blank=True, null=True)
    doc_id = models.IntegerField("Original document ID", editable=False, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    tags = ArrayField(models.CharField(max_length=200), blank=True, null=True)
    url = models.URLField(blank=True, null=True)

    def __repr__(self):
        return self.meta.get('url', self.pk)


class Embed(models.Model):
    page = models.ForeignKey(Page, related_name='embeds')
    uri = models.URLField(blank=True, null=True)


class PageMeta(BaseModel):
    name = models.CharField("Meta field name", max_length=200)
    slug = models.SlugField("Meta field slug")
    pages = models.ManyToManyField(Page)

    def __repr__(self):
        return self.name
