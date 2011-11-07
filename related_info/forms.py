from django import forms
from django.forms.widgets import Textarea


class RelatedUriForm(forms.Form):
    uri = forms.CharField(max_length=255)
    title = forms.CharField(max_length=255)
    notes = forms.CharField(widget=Textarea)


class RelatedPublicationForm(forms.Form):
    uri = forms.CharField(max_length=255)
    title = forms.CharField(max_length=255)
    notes = forms.CharField(widget=Textarea, required=False)
