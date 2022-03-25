from django import forms
from django.forms import ModelForm,TextInput, EmailInput,NumberInput
from .models import Member

# creating a form
class UserProfileForm(ModelForm):
    class Meta:
        model = Member
        fields = ["first_name", "last_name", "phone", "address_1", "city", "state", "email","zip_code", "age_group"]

        help_texts = {
            'first_name': None,
            'last_name': None,
            'phone': None,
            'address_1': None,
            'city': None,
            'state': None,
            'zip_code': None,
            'age_group': None
        }

        widgets = {
            'first_name': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Enter your First Name'
                }),
            'last_name': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Enter your First Name'
                }),
            'phone': NumberInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Enter your Phone Number'}),

            'address_1': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Enter your Address'
                }),
            'city': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Enter your City'
                }),
            'state':TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Enter your State'
                }),
            'zip_code':TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Enter your ZipCode'
                }),
            'age_group':forms.Select(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Enter your ZipCode'
                }),
            'email':EmailInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px; display: none',
                })
            }