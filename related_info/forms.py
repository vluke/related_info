from django import forms
from django.forms.widgets import Textarea

# http://ands.org.au/guides/cpguide/cpgrelatedinfo.html
IDENTIFIER_TYPE_CHOICES = tuple([
    ('', ''),
    ('ark', 'ARK Persistent Identifier Scheme'),
    ('doi', 'Digital Object Identifier'),
    ('ean13', 'International Article Number'),
    ('eissn', 'electronic International Standard Serial Number'),
    ('handle', 'HANDLE System Identifier'),
    ('infouri', "'info' URI Scheme"),
    ('local', 'identifier unique within a local context'),
    ('purl', 'Persistent Uniform Resource Locator'),
    ('uri', 'Uniform Resource Identifier'),
    ('issn', 'International Standard Serial Number'),
    ('isbn', 'International Standard Book Number'),
    ('istc', 'International Standard Text Code'),
    ('lissn', 'linking ISSN (ISSN-L)'),
    ('upc', 'Universal Product Code'),
    ('urn', 'Uniform Resource Name')
])
TYPE_CHOICES = tuple([
    ('', ''),
    ('website', 'website'),
    ('publication', 'publication')
])


class RelatedInfoForm(forms.Form):
    type = forms.CharField(required=False,
                            widget=forms.Select(choices=TYPE_CHOICES))
    identifier_type = forms.CharField(widget=forms.Select(choices=IDENTIFIER_TYPE_CHOICES))
    identifier = forms.CharField(max_length=255)
    title = forms.CharField(required=False, max_length=255)
    notes = forms.CharField(required=False, widget=Textarea)
