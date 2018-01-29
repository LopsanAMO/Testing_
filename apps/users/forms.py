from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import Address


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = (
            'country', 'region', 'town', 'neighborhood', 'zip_code', 'street',
            'street_number', 'suite_number'
        )
        label = {
            'country': _(''),
            'region': _(''),
            'town': _(''),
            'neighborhood': _(''),
            'zip_code': _(''),
            'street': _(''),
            'street_number': _(''),
            'suite_number': _('')
        }
        widgets = {
            'country': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'hidden',
                'value': 'Mexico'
            }),
            'region': forms.TextInput(attrs={
                'placeholder': 'Estado',
                'class': 'form-control',
                'required-field': True
            }),
            'town': forms.TextInput(attrs={
                'placeholder': 'Delegacion',
                'class': 'form-control',
                'required-field': True
            }),
            'neighborhood': forms.TextInput(attrs={
                'placeholder': 'colonia',
                'class': 'form-control',
                'required-field': True
            }),
            'zip_code': forms.TextInput(attrs={
                'placeholder': 'Codigo Postal',
                'class': 'form-control',
                'required-field': True
            }),
            'street': forms.TextInput(attrs={
                'placeholder': 'Calle',
                'class': 'form-control',
                'required-field': True
            }),
            'street_number': forms.TextInput(attrs={
                'placeholder': 'Numero exterior',
                'class': 'form-control',
                'required-field': True
            }),
            'suite_number': forms.TextInput(attrs={
                'placeholder': 'Numero interior',
                'class': 'form-control',
                'required-field': False
            }),
        }
