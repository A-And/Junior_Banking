import logging
from datetime import date

from django.core.exceptions import PermissionDenied
from django.shortcuts import render_to_response, render, redirect

from login.forms import LoginForm, TransferForm, CreateGoalForm, ChildRegistrationForm
from main.restAPI import restAPI
from login.utils import validate_response

"""
    Each view is called in accordance with urls.py. I've added html files just in case.
"""


# Landing_Page.html
def landing(request):
    # If a form is submitted
    if request.method == 'POST':
        form = LoginForm(request.POST)
        # Validate form
        if form.is_valid():
            rest = restAPI("")
            requested_data = rest.login(form.cleaned_data['email'], form.cleaned_data['password'])
            # Re-render the form with an error flag
            if requested_data.status_code != 200:
                form = LoginForm()
                return render(request, 'Landing_Page.html', {'form': form, 'error':True })

            # Invalid login
            if requested_data.json()['status'] == 3:
                form = LoginForm()
                return render(request, 'Landing_Page.html', {'form': form, 'error':True })

            # Parse recieved data
            data = requested_data.json()['data']
            # Set session variables. In this case a cookie and a userID
            request.session['sessionID'] = data['sessionID']
            request.session['userID'] = data['userID']

            rest = restAPI(data['sessionID'])

            # Check the type of account and redirect respectively
            if not rest.is_child(data['userID']):
                return redirect(parent)
            else:
                return redirect(home)

    else:
        # We've received a GET request. Render normally
        form = LoginForm()

    return render(request, 'Landing_Page.html', {'form': form, })


# Accounts.html
def account(request):
    # Verify cookie and user id
    if 'userID' not in request.session or 'sessionID' not in request.session:
        raise PermissionDenied()
    user_id = request.session['userID']
    rest = restAPI(request.session['sessionID'])

    if request.method == 'POST':
        # POST method. Check forms
        form = TransferForm(request.POST)
        if form.is_valid():
            b_to_s = form.cleaned_data['balance_to_stash'] or 0
            s_to_b = form.cleaned_data['stash_to_balance'] or 0
            # Execute transfer
            rest.balance_stash_transfer(user_id, float(b_to_s), float(s_to_b))
        # Get basic informaton
        profile = rest.get_profile(user_id)
        validate_response(profile)
        name = profile['forename'] + " " + profile['surname']
        balance = profile['balance']
        stash = profile['stash']
        # Reset form and render
        form = TransferForm()
        return render(request, 'Accounts.html', {'name': name,
                                                 'balance': balance,
                                                 'stash': stash,
                                                 'form': form, })

    else:
        # GET request. Render normally
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


# home.html
def home(request):
    # Verify cookie and user id
    if 'userID' not in request.session or 'sessionID' not in request.session:
        raise PermissionDenied()
    # Get basic information
    user_id = request.session['userID']
    rest = restAPI(request.session['sessionID'])
    profile = rest.get_profile(user_id)
    # validate the response
    validate_response(profile)
    name = profile['forename'] + " " + profile['surname']
    return render(request, 'home.html', {'name': name})


""" View was removed due to being useless. Kept fpr testing and mesing around """
def profile(request):
    user_id = request.session['userID']
    rest = restAPI(request.session['sessionID'])
    profile = rest.get_profile(user_id)
    validate_response(profile)
    name = profile['forename'] + " " + profile['surname']
    dob = profile['dob']
    return render(request, 'profile.html', {'name': name, 'dob': dob})

# goals.html
def goals(request):
    # Verify cookie and user id
    if 'userID' not in request.session or 'sessionID' not in request.session:
        raise PermissionDenied()
    user_id = request.session['userID']
    rest = restAPI(request.session['sessionID'])
    # Get all valid goals
    returned_goals = rest.get_goals(user_id)
    validate_response(returned_goals)
    stash = rest.get_profile(user_id)['stash']
    # Loop through and build a map we need for rendering.
    total_goal_progress = 0.0
    for value in returned_goals.items():
        goal = value[1]
        if float(goal['target']) - float(goal['progress']) <= 0:
            goal['reached'] = True
        else:
            goal['reached'] = False
        total_goal_progress += float(goal['progress'])


    total = stash + total_goal_progress
    available = stash - total_goal_progress
    return render(request, 'goals.html', {'goals': returned_goals, 'total': round(total,2), 'available': round(available,2),
                                          'sorted_goals': sorted(returned_goals.items())})


# Logout view. Not an actual view, but a helper
def logout(request):
    # Remove and drop session and user
    if 'sessionID' not in request.session:
        return redirect(landing)
    restAPI(request.session['sessionID']).logout()
    del request.session['sessionID']
    del request.session['userID']
    # Redirect to beginning
    return redirect(landing)

# Guide.html
def guide(request):
    # Verify sesion and user
    if 'userID' not in request.session or 'sessionID' not in request.session:
        raise PermissionDenied()
    return render(request, 'guide.html', {
    })

# ATMs.html
def ATMs(request):
    # Verify sesion and user
    if 'userID' not in request.session or 'sessionID' not in request.session:
        raise PermissionDenied()
    user_id = request.session['userID']
    rest = restAPI(request.session['sessionID'])
    # Get atms for rendering
    atms = rest.get_atms(user_id)
    return render(request, 'ATMs.html', {'atms': atms,
    })

# Collections.html
def collection(request):
    # As always, verify
    if 'userID' not in request.session or 'sessionID' not in request.session:
        raise PermissionDenied()

    rest = restAPI(request.session['sessionID'])
    user_id = request.session['userID']
    child_data = rest.get_allgoals(user_id)
    # Create a table count for goals
    counter = 0
    completedTable = {}
    # Loop through and check for completed goals
    for goal in child_data.items():
        if int(goal[1]['completed']) == 1:
            counter += 1
            completedTable[len(completedTable) + 1] = {'desc': goal[1]['desc'],
                                                       'date': date.fromtimestamp(goal[1]['date'])}
    # Get tables for trading cards and bonuses
    cards = rest.get_cards(user_id)
    card_counter = len(cards)

    bonuses = rest.get_lloyds_bonuses(user_id)
    bonuses_counter = len(bonuses)
    return render(request, 'collection.html', {'goalscounter': counter, 'goalscompleted': completedTable, 'cards':cards, 'cardcounter':card_counter, 'bonuses':bonuses, 'bonusescounter':bonuses_counter,
    })

def references(request):
    return render(request, 'references.html')

# PARENT VIEWS

"""


Parent is a very large view, coping with a lot of different types of forms.


"""
def parent(request):
    if 'userID' not in request.session or 'sessionID' not in request.session:
        raise PermissionDenied()
    user_id = request.session['userID']
    rest = restAPI(request.session['sessionID'])
    # Check if the logged in user is a child. If not they don't have permission
    if rest.is_child(user_id):
        raise PermissionDenied()
    # Check the post paramaters. If POST request handle the form
    if request.method == 'POST':
        # Check to see if the delete ATMS form was invoked
        """This is a hacky solution. It's not best practice, but is far more secure
        because we don't need to store any customer data in a database. """
        # If delete was called
        if request.POST.get('deleteatms', False):
            # Loop through return values and skip the token and form name
            for key, value in request.POST.items():
                if key != 'deleteatms' and key != 'csrfmiddlewaretoken':
                    # We've passed the id of an ATM as a key and it's location as a value. This is hacky
                    rest.delete_atm(key, value)
                    # Redirect to view itself
                    return redirect(parent)

        # Check if addatms was called
        if request.POST.get('addatm', False):
            target_id = request.POST.get('targetID', False)
            location = request.POST.get('location', False)
            if target_id and location:
                response = rest.add_atm(user_id, target_id, location)
        # Again, similarly check what has been called
        origin_id = request.POST.get('from', False)
        target_id = request.POST.get('to', False)
        amount = request.POST.get('amount', False)
        if origin_id and target_id and amount:
            # We have all the values: transfer money
            response = rest.transfer_money(origin_id, target_id, amount)
        else:
            # The only valid Django form
            form = CreateGoalForm(request.POST)
            goal_target = request.POST.get('goal_target', False)
            if form.is_valid() and goal_target is not False:
                response = rest.create_goal(user_id, goal_target, form.cleaned_data['goal_description'], form.cleaned_data['goal_amount'])


    child_data = rest.get_children(user_id)
    parent_data = rest.get_profile(user_id)
    validate_response(child_data)
    validate_response(parent_data)

    # Get IDs. Empty list will hold ID values for display


    # Get goals. Empty dictionary will hold all goals
    all_goals = dict()
    counter = 0
    completed_table = {}
    total_atms = list()
    # Loop through returned children
    for key, value in child_data.items():
        atms = {}
        # Append id
        child_id = value['accountID']
        # Get all goals
        child_goals = rest.get_allgoals(child_id)
        child_atms = rest.get_atms(child_id)
        atms['child']= value['forename'] + ' ' + value['surname']
        atms['childID'] = child_id
        atms['atms'] = child_atms
        total_atms.append(atms)
        # Check if goals are completed and if so add them to the final table
        for goal in child_goals.items():
            if int(goal[1]['completed']) == 1:
                counter += 1
                completed_table[len(completed_table) + 1] = {'desc': goal[1]['desc'],
                                                           'date': date.fromtimestamp(goal[1]['date']),
                                                           'name': rest.get_name(child_id)}
    form = CreateGoalForm()
    return render(request, 'parent_account.html', {'child_data': child_data, 'parent_data': parent_data, 'goalscompleted':completed_table,'userID':user_id, 'form':form, 'atms':total_atms})


# signup.html
def signup(request):
    # Verification
    if 'userID' not in request.session or 'sessionID' not in request.session:
        raise PermissionDenied()
    rest = restAPI(request.session['sessionID'])
    # Check if the user has not added more than one child. If so, render form
    if len(rest.get_children(request.session['userID'])) < 2:
        if request.method == 'POST':
            form = ChildRegistrationForm(request.POST)
            if form.is_valid():
                rest = restAPI(request.session['sessionID'])
                response = rest.register_child(request.session['userID'],form.cleaned_data['first_name'], form.cleaned_data['last_name'], form.cleaned_data['dob'], form.cleaned_data['username'], form.cleaned_data['password'])
                redirect(landing)

        form = ChildRegistrationForm()
        return render(request,'sign_up.html',{'form':form})
    else:
         # If a user has two children registered, then he/she cannot register anymore. Redirect to warning
        return render(request, 'sign_up_unavailable.html')

# default 404 override
def http404(request):
    return render_to_response('404.html')

# default 403 override. Also used as a relogin page
def http403(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            rest = restAPI("")
            requestedData = rest.login(form.cleaned_data['email'], form.cleaned_data['password'])
            validate_response(requestedData)
            if requestedData.status_code != 200:
                form = LoginForm()
                return render(request, '403.html', {'form': form, })

            if requestedData.json()['status'] == 3:
                form = LoginForm()
                return render(request, '403.html', {'form': form, })


            # TODO
            data = requestedData.json()['data']
            request.session['sessionID'] = data['sessionID']
            request.session['userID'] = data['userID']

            rest = restAPI(data['sessionID'])

            # TODO Add check for parent account type
            if rest.is_child(data['userID']):
                return redirect(account)
            else:
                return redirect(parent)
        else:
            return redirect(http404)
    else:
        form = LoginForm()

    return render(request, '403.html', {'form': form, })

