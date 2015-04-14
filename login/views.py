import requests
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
        if form.is_valid():
            api_url = settings.API_URL

            post_values = {
                'appid': settings.API_KEY,
                'username': form.cleaned_data['email'],
                'password': form.cleaned_data['password']
            }

            print(post_values)
            logger = logging.getLogger(__name__)
            """ THIS IS WHERE THE MAGIC HAPPENS. Commented out, so that it doesn't throw errors when the API isn't up. Cookie is assigned an arbitrary value"""
            LOGIN_URL = 'login'
            requestedData = requests.post(api_url+LOGIN_URL, data=post_values)
            logger.debug(api_url + LOGIN_URL)
            logger.debug(requestedData.status_code)

            if requestedData.status_code != 200:
                form = LoginForm()
                return render(request, 'Landing_Page.html', {'form': form, })

            logger.debug(requestedData)

            logger.debug(requestedData.json())

            if requestedData.json()['status'] == 3:
                form = LoginForm()
                return render(request, 'Landing_Page.html', {'form': form, })


            # TODO
            data = requestedData.json()['data']
            print(data) 
            cookieID = data['sessionID']
            userID = data['userID']
            request.session['sessionID'] = cookieID
            return redirect(account, user_id=userID)

    else:
        form = LoginForm()

    return render(request, 'Landing_Page.html', {'form': form, })


def account(request, user_id):
    rest = restAPI(request.session['sessionID'])
    profile = rest.get_profile(user_id)
    print(profile)
    name = profile['forename'] + " " + profile['surname']
    balance = profile['balance']
    stash = 0
    return render(request, 'Accounts.html', {'name': name,
                                             'balance': balance,
                                             'stash': stash})

def profile(request, user_id):
    rest = restAPI(user_id)
    name = restAPI.get_name(user_id)
    return render(request, 'profile.html', {
        'name': name,
    })



def http404(request):
    return render_to_response('404.html')

