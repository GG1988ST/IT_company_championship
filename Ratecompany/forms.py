from django import forms
from Ratecompany.models import Company, Comments, Category
from django.contrib.auth.models import User


class CompanyForm(forms.ModelForm):
    name = forms.CharField(max_length=Company.NAME_MAX_LENGTH, help_text="Please enter the category name.")
    location = forms.CharField(max_length=Company.NAME_MAX_LENGTH,)
    rates = forms.IntegerField(widget=forms.HiddenInput(),initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(),initial=0)
    slug= forms.CharField(widget=forms.HiddenInput(), required=False)

    #for additional information on the form nested class
    class Meta:
        # provide on association between the ModelForm and a model
        model = Company
        # This means specifying only the name field?
        fields = ('name','location')


class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length= Category.TAB_MAX_LENGTH, help_text="Please enter the category name.")

    class Meta:
        model = Category
        fields = ('name',)




