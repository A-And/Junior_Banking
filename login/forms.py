
# -*- coding: utf-8 -*-
import re
from django.core.validators import RegexValidator

__author__ = 'Andon'
 
from django import forms
 
 
class LoginForm(forms.Form):
 
    email = forms.CharField(label='Username', max_length=50, widget=forms.TextInput(attrs={'class': "input_field"}))
    password = forms.CharField(label='Password', max_length=50, widget=forms.PasswordInput(attrs={'class': "input_field"}))
 
 
class TransferForm(forms.Form):

    decimal = re.compile(r'[^\d.]+')
    numerical_validator = RegexValidator(regex = '[^\d.]+$',
                                         message = 'Please enter valid amount',
                                         code = 'invalid_amount')
    stash_to_balance = forms.CharField(max_length = 5, validators=[numerical_validator], widget = forms.TextInput(attrs={'name': 'stash-to-balance', 'placeholder': '￡' }))
    balance_to_stash = forms.CharField(max_length = 5, validators=[numerical_validator], widget = forms.TextInput(attrs={'name': 'balance-to-stash', 'placeholder': '￡'}))
