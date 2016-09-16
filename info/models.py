
import uuid
from django.db import models
from django.contrib.postgres.fields import HStoreField, JSONField, ArrayField
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


class Page(BaseModel):
    language = models.CharField(max_length=3)
    meta = HStoreField(blank=True, null=True)
    collection = models.ForeignKey(MasterPage)


