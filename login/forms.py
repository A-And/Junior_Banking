
# -*- coding: utf-8 -*-
import re

__author__ = 'Andon'
 
from django import forms
 
 
class LoginForm(forms.Form):
 
    email = forms.CharField(label='Username', max_length=50, widget=forms.TextInput(attrs={'required':'required', 'class': "input_field"}))
    password = forms.CharField(label='Password', max_length=50, widget=forms.PasswordInput(attrs={'required':'required','class': "input_field"}))
 
 
class TransferForm(forms.Form):

    stash_to_balance = forms.FloatField(required=False,widget = forms.TextInput(attrs={'name': 'stash-to-balance', 'placeholder': '￡' }))
    balance_to_stash = forms.FloatField(required=False,widget = forms.TextInput(attrs={'name': 'balance-to-stash', 'placeholder': '￡'}))
