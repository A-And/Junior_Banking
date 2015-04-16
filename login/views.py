import logging

from django.core.exceptions import PermissionDenied

from django.shortcuts import render_to_response, render, redirect

from login.forms import LoginForm, TransferForm, ParentChildTransferForm, CreateGoalForm, ChildRegistrationForm

from main.restAPI import restAPI

from login.utils import validate_response
from datetime import date


def landing(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            rest = restAPI("")
            requestedData = rest.login(form.cleaned_data['email'], form.cleaned_data['password'])

            logger = logging.getLogger(__name__)

            print(requestedData.status_code)

            if requestedData.status_code != 200:
                form = LoginForm()
                return render(request, 'Landing_Page.html', {'form': form, 'error':True })

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
        print(form.is_valid())
        if form.is_valid():
            b_to_s = form.cleaned_data['balance_to_stash'] or 0
            s_to_b = form.cleaned_data['stash_to_balance'] or 0

            rest.balance_stash_transfer(user_id, float(b_to_s), float(s_to_b))

        profile = rest.get_profile(user_id)
        validate_response(profile)
        name = profile['forename'] + " " + profile['surname']
        balance = profile['balance']
        stash = profile['stash']
        form = TransferForm()
        return render(request, 'Accounts.html', {'name': name,
                                                 'balance': balance,
                                                 'stash': stash,
                                                 'form': form, })

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
                                                 'form': form })


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
    rest = restAPI(request.session['sessionID'])
    print("REST IS")
    print(rest)
    name = rest.get_name(user_id)
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
    return render(request, 'goals.html', {'goals': returned_goals, 'total': total, 'available': available,
                                          'sorted_goals': sorted(returned_goals.items())})


def logout(request):
    restAPI(request.session['sessionID']).logout()
    del request.session['sessionID']
    del request.session['userID']
    return redirect(landing)


def guide(request):
    return render(request, 'guide.html', {
    })


def ATMs(request):
    user_id = request.session['userID']
    rest = restAPI(request.session['sessionID'])
    atms = rest.get_atms(user_id)
    return render(request, 'ATMs.html', {'atms': atms,
    })


def collection(request):
    if request.GET.get('logout'):
        restAPI(request.session['sessionID']).logout()
        redirect(landing(request))

    rest = restAPI(request.session['sessionID'])
    user_id = request.session['userID']
    child_data = rest.get_allgoals(user_id)

    counter = 0
    completedTable = {}

    for goal in child_data.items():
        if int(goal[1]['completed']) == 1:
            counter += 1
            completedTable[len(completedTable) + 1] = {'desc': goal[1]['desc'],
                                                       'date': date.fromtimestamp(goal[1]['date'])}

    return render(request, 'collection.html', {'goalscounter': counter, 'goalscompleted': completedTable
    })

# PARENT VIEWS
def parent(request):
    if 'userID' not in request.session or 'sessionID' not in request.session:
        raise PermissionDenied()
    user_id = request.session['userID']
    rest = restAPI(request.session['sessionID'])
    # Check if the logged in user is a child. If not they don't have permission
    if rest.is_child(user_id):
        raise PermissionDenied()
    # Check the post paramaters
    if request.method == 'POST':
        print('-----------------------------------------------------')
        origin_id = request.POST.get('from', False)
        target_id = request.POST.get('to', False)
        amount = request.POST.get('amount', False)
        if origin_id and target_id and amount:
            response = rest.transfer_money(origin_id, target_id, amount)
            print(response)
        else:

            form = CreateGoalForm(request.POST)
            goal_target = request.POST.get('goal_target', False)
            print(form.is_valid())
            if form.is_valid() and goal_target is not False:
                response = rest.create_goal(user_id, goal_target, form.cleaned_data['goal_description'], form.cleaned_data['goal_amount'])
                print(response)

    child_data = rest.get_children(user_id)
    parent_data = rest.get_profile(user_id)
    validate_response(child_data)
    validate_response(parent_data)
    print(parent_data)
    print(child_data.items())

    # Get IDs. Empty list will hold ID values for display


    # Get goals. Empty dictionary will hold all goals
    all_goals = dict()
    counter = 0
    completed_table = {}
    # Loop through returned children
    for key, value in child_data.items():
        # Append id
        child_id = value['accountID']
        # Get all goals
        child_goals = rest.get_allgoals(child_id)
        # Check if goals are completed and if so add them to the final table
        for goal in child_goals.items():
            if int(goal[1]['completed']) == 1:
                counter += 1
                completed_table[len(completed_table) + 1] = {'desc': goal[1]['desc'],
                                                           'date': date.fromtimestamp(goal[1]['date']),
                                                           'name': rest.get_name(child_id)}
    form = CreateGoalForm()
    return render(request, 'parent_account.html', {'child_data': child_data, 'parent_data': parent_data, 'goalscompleted':completed_table,'userID':user_id, 'form':form})


def signup(request):
    form = ChildRegistrationForm()
    return render(request,'sign_up.html',{'form':form})

def http404(request):
    return render_to_response('404.html')


def http403(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            rest = restAPI("")
            requestedData = rest.login(form.cleaned_data['email'], form.cleaned_data['password'])
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
            if rest.is_child(data['userID']):
                return redirect(account)
            else:
                return redirect(parent)

    else:
        form = LoginForm()

    return render(request, '403.html', {'form': form, })

