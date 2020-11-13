from django import forms
from .models import CategoryChoices


class NewListingForm(forms.Form):
    title = forms.CharField(required=True, label="Title")
    price = forms.DecimalField(decimal_places=2, required=True, label="Price")
    imageURL = forms.URLField(required=False, label="Image Url")
    category = forms.ChoiceField(
        choices=CategoryChoices.choices, required=True, label="Category")
    description = forms.CharField(
        widget=forms.Textarea, required=False, label="Description")


class NewBidForm(forms.Form):
    bid = forms.DecimalField(
        decimal_places=2, required=True, min_value=1, label="Bid")


class NewCommentForm(forms.Form):
    comments = forms.CharField(widget=forms.Textarea, required=True, label="Your comment")
