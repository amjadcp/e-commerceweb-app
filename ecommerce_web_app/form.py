from django import forms
from django.forms import fields, widgets
from .models import *

class Add_item_form(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('item', 'img', 'price', 'disc', 'category')
        widgets = {
            'Item' : forms.CharField(),
            'Image of Item' : forms.ImageField(),
            'Price' : forms.DecimalField(),
            'Discription' : forms.Textarea(),
            'Category' : forms.Select()
        }

class Add_category_form(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('category',)
        widgets = {
            'Catogory' : forms.CharField()
        }