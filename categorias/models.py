from django.db import models
from core.models import ModelDefault
from model_utils.managers import QueryManager
import uuid


class Categoria(ModelDefault):

    class Meta:
        ordering = ['nome']
    
    nome = models.CharField(max_length=255)
    uuid = models.CharField(default=uuid.uuid4, editable=False, max_length=200, db_index=True)
    
    objects = QueryManager(data_cancelamento__isnull=True)
    
    def __str__(self):
        return self.nome
