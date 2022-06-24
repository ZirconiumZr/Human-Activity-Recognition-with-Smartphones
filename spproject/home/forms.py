from distutils.command.upload import upload
from django import forms
from django.forms import widgets
# from matplotlib.pyplot import cla


from .models import CsvUpload


class CsvUploadForm(forms.ModelForm):
  class Meta:
    model = CsvUpload
    fields = ("csv_file",)
