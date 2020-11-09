from django import forms
from .models import CategoryChoices


class NewListingForm(forms.Form):
    title = forms.CharField(required=True)
    price = forms.DecimalField(decimal_places=2, required=True)
    imageURL = forms.URLField(required=False)
    category = forms.ChoiceField(choices=CategoryChoices.choices,required=True)
    description = forms.CharField(widget=forms.Textarea, required=False)

class NewBidForm(forms.Form):
    bid=forms.DecimalField(decimal_places=2,required=True)