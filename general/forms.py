from django import forms
from django.contrib.auth.models import User
from general.models import UserAccount
from general.modelchoices import *
# from tinymce.models import HTMLField
from general.models import UserAccount, Category, Item



attrs3 = {'class': 'form-control', 'required': 'required'}

class DateInput(forms.DateInput):
    input_type = 'date'


class UserForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class ItemForm(forms.ModelForm):
	name = forms.CharField(widget=forms.TextInput(attrs=attrs3))
	description = forms.CharField(widget=forms.TextInput(attrs=attrs3))
	class Meta:
	    model = Item
	    fields = ('name', 
	    	'description', 
	    	'category', 
	    	'weight', 
	    	'tag', 
	    	'sub_category', 
	    	'quantity', 
	    	'price',
	    	'shipping_cost_USA',
	    	'shipping_cost_NGN',
	    	'item_image_small',
	    	'item_image_big',)


class CategoryForm(forms.ModelForm):

	category_name = forms.CharField(help_text="Category Name", required=True,
	                             widget=forms.TextInput(attrs={'required': 'required'}))

	class Meta:
	    model = Category
	    fields = ('category_name',)