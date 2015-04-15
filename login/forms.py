
# -*- coding: utf-8 -*-
import re

__author__ = 'Andon'
 
from django import forms
 
 
class LoginForm(forms.Form):
 
    email = forms.CharField(label='Username', max_length=50, widget=forms.TextInput(attrs={'class': "input_field"}))
    password = forms.CharField(label='Password', max_length=50, widget=forms.PasswordInput(attrs={'class': "input_field"}))
 
 
class TransferForm(forms.Form):

    decimal = re.compile(r'[^\d.]+')
    stash_to_balance = forms.IntegerField(widget = forms.TextInput(attrs={'name': 'stash-to-balance', 'placeholder': '￡' }))
    balance_to_stash = forms.IntegerField(widget = forms.TextInput(attrs={'name': 'balance-to-stash', 'placeholder': '￡'}))
