import urllib.parse
import urllib.request
import logging
import json
from django.shortcuts import render_to_response, render, redirect
from django.template import loader, RequestContext
from django.conf import settings
from login.forms import LoginForm
from main.restAPI import restAPI


def landing(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        logger = logging.getLogger(__name__)
        if form.is_valid():
            api_url = settings.API_URL

            post_values = {
                'appid': settings.API_KEY,
                'user': form.cleaned_data['email'],
                'password': form.cleaned_data['password']
            }

            """ THIS IS WHERE THE MAGIC HAPPENS. Commented out, so that it doesn't throw errors when the API isn't up. Cookie is assigned an arbitrary value"""
            LOGIN_URL = 'login'
            logger.debug(post_values)
            post_data = urllib.parse.urlencode(post_values).encode('ascii')
            logger.debug(post_data)
            req = urllib.request.Request(api_url + LOGIN_URL, post_data)
            logger.debug(api_url + LOGIN_URL)
            response = urllib.request.urlopen(req)
            page = response.read()
            data = json.load(page)
            cookieID = data['sessionID']
            request.session['sessionID'] = cookieID
            logger.debug(page)
            return redirect(account, user_id=cookieID)

    else:
        form = LoginForm()

    return render(request, 'Landing_Page.html', {'form': form, })


def account(request, user_id):
    rest = restAPI(user_id)
    name = rest.get_name()
    balance = rest.get_balance()
    stash = rest.get_stash()
    return render(request, 'Accounts.html', {'name': name,
                                             'balance': balance,
                                             'stash': stash})


def http404(request):
    return render_to_response('404.html')

