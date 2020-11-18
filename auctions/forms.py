from django import forms
from .models import CategoryChoices

#Multiple ways to add class to forms
class NewListingForm(forms.Form):
    title = forms.CharField(required=True, label="Title")
    price = forms.DecimalField(decimal_places=2, required=True, label="Price")
    imageURL = forms.URLField(required=False, label="Image Url")
    category = forms.ChoiceField(
        choices=CategoryChoices.choices, required=True, label="Category")
    description = forms.CharField(
        widget=forms.Textarea, required=False, label="Description")

    def __init__(self, *args, **kwargs):
        super(NewListingForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update(
            {'class': 'form-control mx-sm-3 mb-2'})
        self.fields['price'].widget.attrs.update(
            {'class': 'form-control mx-sm-3 mb-2'})
        self.fields['imageURL'].widget.attrs.update(
            {'class': 'form-control mx-sm-3 mb-2'})
        self.fields['category'].widget.attrs.update(
            {'class': 'form-control mx-sm-3 mb-2'})
        self.fields['description'].widget.attrs.update(
            {'class': 'form-control mx-sm-3 mb-2 txtfield'})


class NewBidForm(forms.Form):
    bid = forms.DecimalField(
        decimal_places=2, required=True, min_value=1, label="Bid")
    bid.widget.attrs.update({'class': 'form-control mx-sm-2'})


class NewCommentForm(forms.Form):
    comments = forms.CharField(
        widget=forms.Textarea(attrs={'class' : 'form-control sm-3 mb-2 txtfield'}), required=True, label="Your comment")
    


class NewCategoryForm(forms.Form):
    category = forms.ChoiceField(
        choices=CategoryChoices.choices, required=True, label="Category")

    def __init__(self, *args, **kwargs):
        super(NewCategoryForm, self).__init__(*args, **kwargs)
        self.fields['category'].widget.attrs.update(
            {'class': 'form-control mx-sm-2'})
