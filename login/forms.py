__author__ = 'Andon'

from django import forms


class LoginForm(forms.Form):

    email = forms.CharField(label='Username', max_length=50, widget=forms.TextInput(attrs={'class': "input_field"}))
    password = forms.CharField(label='Password', max_length=50, widget=forms.PasswordInput(attrs={'class': "input_field"}))


class TransferForm(forms.Form):
    stash_to_pocket = forms.CharField(max_length = 5, widget = forms.TextInput(attrs={'id':'leftarrow',}))
    pocket_to_stash = forms.CharField(max_length = 5, widget = forms.TextInput(attrs={'id':'rightarrow',}))