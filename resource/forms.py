from django import forms
from resource.models import Resource

# creates the resource form for uploading
class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ['document', 'filename']