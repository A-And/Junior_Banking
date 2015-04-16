
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


class ParentChildTransferForm(forms.Form):
    from_account =  forms.ChoiceField(label="From", choices=(),
                                       widget=forms.Select(attrs={'class':'selector', 'name':'from'}))

    to_account = forms.ChoiceField(label="To", choices=(),
                                       widget=forms.Select(attrs={'class':'selector', 'name':'to'}))

    def __init__(self, accounts, *args, **kwargs):
        super(ParentChildTransferForm, self).__init__(*args, **kwargs)
        self.fields['from_account'].choices = accounts
        self.fields['to_account'].choices = accounts