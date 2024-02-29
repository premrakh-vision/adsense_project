from django import forms
from .models import StaticFile

class StaticFileForm(forms.ModelForm):
    class Meta:
        model = StaticFile
        fields = ['file_name','file']