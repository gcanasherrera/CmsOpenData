
from django import forms

class SSHForm(forms.Form):
    ssh_key = forms.CharField(widget=forms.Textarea(attrs={'cols': 100,
                                                           'rows': 6}),
                              required=False, label="")

class OntologyForm(forms.Form):
    