from django import forms


class NewListingForm(forms.Form):
    title = forms.CharField(required=True)
    bid = forms.DecimalField(decimal_places=2, required=True)
    imageURL = forms.URLField()
    category = forms.ChoiceField(choices=(),required=True)
    description = forms.CharField(widget=forms.Textarea, required=True)