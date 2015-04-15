
# -*- coding: utf-8 -*-
import re
 
__author__ = 'Andon'
 
from django import forms
 
 
class LoginForm(forms.Form):
 
    email = forms.CharField(label='Username', max_length=50, widget=forms.TextInput(attrs={'class': "input_field"}))
    password = forms.CharField(label='Password', max_length=50, widget=forms.PasswordInput(attrs={'class': "input_field"}))
 
 
class TransferForm(forms.Form):
    stash_to_balance = forms.CharField(max_length = 5, initial='￡', widget = forms.TextInput(attrs={'name': 'stash-to-balance', }))
    balance_to_stash = forms.CharField(max_length = 5, initial='￡', widget = forms.TextInput(attrs={'name': 'balance-to-stash', }))
 
    def is_valid(self):
        # Check if the amount entered is a valid number. This regex matches digits (including floating point numbers
        decimal = re.compile(r'[^\d.]+')
        super().clean()

        s_to_b = super.cleaned_data['stash_to_balance']
        b_to_s = super.cleaned_data['balance_to_stash']
 
        if decimal.match(s_to_b) and decimal.match(b_to_s):
            return True
        else:
            self._errors['invalid_input'] = 'Invalid input'
            return False