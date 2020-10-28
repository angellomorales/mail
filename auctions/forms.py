from django import forms

class NewListingForm(forms.Form):
    title = forms.CharField(label="title", required=True)
    content = forms.CharField(widget=forms.Textarea,
                              label="content", required=True)