
from dataclasses import field
from django.db.models import fields
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, widgets
from django.contrib.auth.models import User
from django import forms
from .models import *

class UserRegistrationForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'input-field', 'autocomplete':'off', 'placeholder':'Username'})
        self.fields['first_name'].widget.attrs.update({'class': 'input-field', 'autocomplete':'on', 'placeholder':'First name'})
        self.fields['last_name'].widget.attrs.update({'class': 'input-field', 'autocomplete':'on', 'placeholder':'Last name'})
        self.fields['email'].widget.attrs.update({'class': 'input-field', 'autocomplete':'on', 'placeholder':'Email'})
        self.fields['password'].widget.attrs.update({'class': 'input-field', 'autocomplete':'off', 'placeholder':'Set password'})

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }
        help_texts = {
            'username': None
        }


class UserLoginForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'input-field', 'autocomplete':'off', 'placeholder':'username'})
        self.fields['password'].widget.attrs.update({'class': 'input-field', 'autocomplete':'off', 'placeholder':'set password'})

    
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'password':forms.PasswordInput(),
        }
        help_texts = {
            'username': None
        }



