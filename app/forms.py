from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

class CustomerRegistrationForm(UserCreationForm):
    password1 = forms.CharField(label_suffix='Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Confirm Pasword', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    email = forms.CharField(required=True, widget=forms.EmailInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {'email': 'Email'}
        widgets = {'username' : forms.TextInput(attrs={'class' : 'form-control'})}


class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'locality', 'city', 'state', 'phone', 'zipcode']
        widgets = {'name' : forms.TextInput(attrs={'class':'form-control'}),
         'locality':forms.TextInput(attrs={'class':'form-control'}), 'city':forms.TextInput(attrs={'class':'form-control'}),
        'phone' : forms.NumberInput(attrs={'class':'form-control'}), 'state' : forms.Select(attrs={'class':'form-control'}), 'zipcode' : forms.NumberInput(attrs={'class':'form-control'}),}