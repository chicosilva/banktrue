from django.db import models
from uuid import uuid4


class CustomManager(models.Manager):
    def get_queryset(self):
        return super(CustomManager, self).get_queryset().filter(canceled_at__isnull=True)


class ModelDefault(models.Model):
    class Meta:
        abstract = True
    
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_at = models.DateTimeField(editable=False, auto_now_add=True)
    canceled_at = models.DateTimeField(editable=False, null=True, blank=True)
    update_at = models.DateTimeField(editable=False, auto_now=True)
    
    objects = CustomManager()
    