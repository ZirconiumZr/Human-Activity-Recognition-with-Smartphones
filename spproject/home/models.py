from django.db import models
from spproject.settings import MEDIA_ROOT
# Create your models here.
class Models(models.Model):
  name = models.CharField(max_length=255)
  accuracy = models.CharField(max_length=255)

class CsvUpload(models.Model):
#   date_uploaded = models.DateTimeField(auto_now=True)
  csv_file = models.FileField(upload_to=MEDIA_ROOT)