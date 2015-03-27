__author__ = 'Andon'

from django import forms


class LoginForm:

    email = forms.CharField(label='email', max_length=50)
    password = forms.CharField(label='password', max_length=50)