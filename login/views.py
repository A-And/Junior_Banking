
import logging
from django.http import Http404

import requests
from django.shortcuts import render_to_response, render, redirect
from django.conf import settings

from login.forms import LoginForm, TransferForm
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
			print(requestedData.status_code)

			if requestedData.status_code != 200:
				form = LoginForm()
				return render(request, 'Landing_Page.html', {'form': form, })

			if requestedData.json()['status'] == 3:
				form = LoginForm()
				return render(request, 'Landing_Page.html', {'form': form, })

			# TODO
			data = requestedData.json()['data']
			print(data)
			request.session['sessionID'] = data['sessionID']
			request.session['userID'] = data['userID']
			# TODO Add check for parent account type
			return redirect(account)

	else:
		form = LoginForm()

	return render(request, 'Landing_Page.html', {'form': form, })


def account(request):

	user_id = request.session['userID']
	rest = restAPI(request.session['sessionID'])
	if request.method == 'POST':
		form = TransferForm(request.POST)
		print('ITS HERE')
		print(form.is_valid())
		if form.is_valid():
			print(form.cleaned_data)
			b_to_s = form.cleaned_data['balance_to_stash'] or 0
			s_to_b = form.cleaned_data['stash_to_balance'] or 0
			rest.balance_stash_transfer(user_id, float(b_to_s), float(s_to_b))

			profile = rest.get_profile(user_id)
			if profile == 403 or profile == 500:
				return redirect(landing)

		name = profile['forename'] + " " + profile['surname']
		balance = profile['balance']
		stash = profile['stash']
		return render(request, 'Accounts.html', {'name': name,
											 'balance': balance,
											 'stash': stash,
											 'form': form,})


	else:
	
		profile = rest.get_profile(user_id)      
		
		if profile == 403 or profile == 500:
			return redirect(landing)
	

		name = profile['forename'] + " " + profile['surname']
		balance = profile['balance']
		stash = profile['stash']
		form = TransferForm()
		return render(request, 'Accounts.html', {'name': name,
											 'balance': balance,
											 'stash': stash,
											 'form': form,})


def home(request):
	user_id = request.session['userID']
	rest = restAPI(request.session['sessionID'])
	profile = rest.get_profile(user_id)
	if profile == 403 or profile == 500:
		return redirect(landing)
	name = profile['forename'] + " " + profile['surname']
	return render(request, 'home.html', {'name': name})


def profile(request):
	user_id = request.session['userID']
	rest = restAPI(user_id)
	name = restAPI.get_name(user_id)
	print(name)
	if 'Error' in name:
		error = name['error']
	return render(request, 'profile.html', {
		'name': name,
	})


def goals(request):
	user_id = request.session['userID']
	rest = restAPI(request.session['sessionID'])
	print(user_id)
	returned_goals = rest.get_goals(user_id)
	if returned_goals == 403 or returned_goals == 500:
		return redirect(landing)
	print(returned_goals)
	return render(request, 'goals.html', {'goals': returned_goals})


def guide(request):
	user_id = request.session['userID']
	rest = restAPI(user_id)
	return render(request, 'guide.html', {
	})

def ATMs(request):
	user_id = request.session['userID']
	rest = restAPI(user_id)
	return render(request, 'ATMs.html', {
	})
	
def collection(request):
	user_id = request.session['userID']
	rest = restAPI(user_id)
	
	return render(request, 'collection.html', {
	})

def http404(request):
	return render_to_response('404.html')

def http403(request):
	return



