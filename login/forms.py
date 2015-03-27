__author__ = 'Andon'

from django import forms


class LoginForm(forms.Form):

    email = forms.CharField(label='email', max_length=50, widget=forms.TextInput(attrs={'class': "input_field"}))
    password = forms.CharField(label='password', max_length=50,   widget=forms.PasswordInput(attrs={'class': "input_field"}))

