import logging

from django.core.exceptions import PermissionDenied
from django.shortcuts import render_to_response, render, redirect

from login.forms import LoginForm, TransferForm
from main.restAPI import restAPI
from login.utils import validate_response

def landing(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            rest = restAPI("")
            requestedData = rest.login( form.cleaned_data['email'], form.cleaned_data['password'])

            logger = logging.getLogger(__name__)

            print(requestedData.status_code)

            if requestedData.status_code != 200:
                form = LoginForm()
                return render(request, 'Landing_Page.html', {'form': form, })

            print(requestedData)

            print(requestedData.json())

            if requestedData.json()['status'] == 3:
                form = LoginForm()
                return render(request, 'Landing_Page.html', {'form': form, })


            # TODO
            data = requestedData.json()['data']
            print('THIS IS IT')
            print(data)
            request.session['sessionID'] = data['sessionID']
            request.session['userID'] = data['userID']

            rest = restAPI(data['sessionID'])

            # TODO Add check for parent account type
            if not rest.is_child(data['userID']):
                return redirect(parent)
            else:
                return redirect(account)

    else:
        form = LoginForm()

    return render(request, 'Landing_Page.html', {'form': form, })


def account(request):
    if 'userID' not in request.session or 'sessionID' not in request.session:
        raise PermissionDenied()
    user_id = request.session['userID']
    rest = restAPI(request.session['sessionID'])
    if request.method == 'POST':
        form = TransferForm(request.POST)
        print('ITS HERE')
        print(form.is_valid())
        if form.is_valid():
            print('valid form')
            print(form.cleaned_data)
            b_to_s = form.cleaned_data['balance_to_stash'] or 0
            s_to_b = form.cleaned_data['stash_to_balance'] or 0
            print('YOU WANT THIS')
            print(b_to_s)
            print(s_to_b)
            rest.balance_stash_transfer(user_id, float(s_to_b), float(b_to_s))

        profile = rest.get_profile(user_id)
        validate_response(profile)
        name = profile['forename'] + " " + profile['surname']
        balance = profile['balance']
        stash = profile['stash']
        return render(request, 'Accounts.html', {'name': name,
                                             'balance': balance,
                                             'stash': stash,
                                             'form': form,})

    else:
        profile = rest.get_profile(user_id)
        validate_response(profile)
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
    validate_response(profile)
    print(profile)
    name = profile['forename'] + " " + profile['surname']
    return render(request, 'home.html', {'name': name})


def profile(request):
    user_id = request.session['userID']
    rest = restAPI(user_id)
    name = restAPI.get_name(user_id)
    validate_response(name)
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

    validate_response(returned_goals)
    stash = rest.get_profile(user_id)['stash']
    total_goal_progress = 0.0
    for value in returned_goals.items():
        goal = value[1]
        print('HEERE')
        if float(goal['target']) - float(goal['progress']) <= 0:
            goal['reached'] = True
        else:
            goal['reached'] = False
        total_goal_progress += float(goal['progress'])

    for value in returned_goals.items():
        if goal['reached']:
            print(goal)
    total = stash + total_goal_progress
    available = stash - total_goal_progress
    print(returned_goals)
    return render(request, 'goals.html', {'goals': returned_goals, 'total': total, 'available': available, 'sorted_goals':sorted(returned_goals.items())})


def logout(request):
    restAPI(request.session['sessionID']).logout()
    del request.session['sessionID']
    del request.session['userID']
    return redirect(landing)


def guide(request):
    return render(request, 'guide.html', {
    })


def parent(request):
    if 'userID' not in request.session or 'sessionID' not in request.session:
        raise PermissionDenied()
    user_id = request.session['userID']
    rest = restAPI(request.session['sessionID'])
    if rest.is_child(user_id):
        raise PermissionDenied()
    child_data = rest.get_children(user_id)
    parent_data = rest.get_profile(user_id)
    validate_response(child_data)
    validate_response(parent_data)
    print(parent_data)
    request.session['childID'] = child_data
    print(child_data.items())
    return render(request, 'parent_account.html', { 'child_data': child_data, 'parent_data':parent_data})


def ATMs(request):
    user_id = request.session['userID']
    rest = restAPI(request.session['sessionID'])
    atms = rest.get_atms(user_id)
    validate_response(atms)
    return render(request, 'ATMs.html', {'atm_list': atms,
    })


def collection(request):
    if request.GET.get('logout'):
        print("REACHED")
        restAPI(request.session['sessionID']).logout()
        redirect(landing(request))
    return render(request, 'collection.html', {
    })


def http404(request):
    return render_to_response('404.html')

def http403(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            rest = restAPI("")
            requestedData = rest.login( form.cleaned_data['email'], form.cleaned_data['password'])
            validate_response(requestedData)
            logger = logging.getLogger(__name__)

            print(requestedData.status_code)

            if requestedData.status_code != 200:
                form = LoginForm()
                return render(request, '403.html', {'form': form, })

            print(requestedData)

            print(requestedData.json())

            if requestedData.json()['status'] == 3:
                form = LoginForm()
                return render(request, '403.html', {'form': form, })


            # TODO
            data = requestedData.json()['data']
            print('THIS IS IT')
            print(data)
            request.session['sessionID'] = data['sessionID']
            request.session['userID'] = data['userID']

            rest = restAPI(data['sessionID'])

            # TODO Add check for parent account type
            if  rest.is_child(data['userID']):
                return redirect(parent)
            else:
                return redirect(account)

    else:
        form = LoginForm()

    return render(request, '403.html', {'form': form, })

