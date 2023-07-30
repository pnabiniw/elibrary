import uuid
from django.db import models


class BaseModel(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class FileUpload(BaseModel):
    file = models.FileField(upload_to='files')
    name = models.CharField(max_length=100)
