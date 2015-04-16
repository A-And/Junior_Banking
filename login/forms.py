# -*- coding: utf-8 -*-
import re
from django.forms import DateInput

__author__ = 'Andon'

from django import forms
from functools import partial


class LoginForm(forms.Form):
    email = forms.CharField(label='Username', max_length=50,
                            widget=forms.TextInput(attrs={'required': 'required', 'class': "input_field"}))
    password = forms.CharField(label='Password', max_length=50,
                               widget=forms.PasswordInput(attrs={'required': 'required', 'class': "input_field"}))


class ChildRegistrationForm(forms.Form):
    DateInput = partial(forms.DateInput, {'class': 'datepicker input_field'})
    username = forms.CharField(label='Usernamegit ', max_length=50,widget=forms.TextInput(attrs={'required':'required', 'class': "input_field"}))
    password = forms.CharField(label='Password', max_length=50,widget=forms.PasswordInput(attrs={'required':'required', 'class': "input_field"}))
    first_name = forms.CharField(label='First Name', max_length=50,widget=forms.TextInput(attrs={'required':'required', 'class': "input_field"}))
    last_name = forms.CharField(label='Last Name', max_length=50,widget=forms.TextInput(attrs={'required':'required', 'class': "input_field"}))
    dob = forms.DateField(label='Date of Birth', widget=DateInput())


class TransferForm(forms.Form):
    stash_to_balance = forms.FloatField(required=False,
                                        widget=forms.TextInput(attrs={'name': 'stash-to-balance', 'placeholder': '￡'}))
    balance_to_stash = forms.FloatField(required=False,
                                        widget=forms.TextInput(attrs={'name': 'balance-to-stash', 'placeholder': '￡', }))


class ParentChildTransferForm(forms.Form):
    from_account = forms.ChoiceField(label="From", choices=(),
                                     widget=forms.Select(attrs={'class': 'selector', 'name': 'from'}))

    to_account = forms.ChoiceField(label="To", choices=(),
                                   widget=forms.Select(attrs={'class': 'selector', 'name': 'to'}))

    def __init__(self, names, *args, **kwargs):
        super(ParentChildTransferForm, self).__init__(*args, **kwargs)
        self.fields['from_account'].choices = names
        self.fields['to_account'].choices = names

class CreateGoalForm(forms.Form):

    goal_description = forms.CharField(label='Description', max_length=50,
                            widget=forms.TextInput(attrs={'required': 'required', 'class': "input_field", 'name': 'goal_description'}))

    goal_amount = forms.FloatField(required=True,label='Goal Points',
                                        widget=forms.TextInput(attrs={'required': 'required', 'class': "input_field", 'name': 'goal_amount'}))
