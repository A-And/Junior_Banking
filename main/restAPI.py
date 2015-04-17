from django.core.exceptions import PermissionDenied
from django.http import Http404
import requests
import logging
from django.conf import settings

__author__ = 'Andon'

"""
    Class to communicate with an API endpoint. Endpoint settings can be found in settings.py
    All of them work in the same basic way - take in arguments and pass them as a POST parameter.
    Afterwards parse the response and send it along.
"""
class restAPI:
    cookie_id = ""

    def __init__(self, cookie_id):
        self.cookie_id = cookie_id

    # Login
    def login(self, username, password):
        data = requests.post(settings.API_URL + 'login', data={
            'appid': settings.API_KEY,
            'username': username,
            'password': password
        })
        return data

    # Logout
    def logout(self):
        data = requests.post(settings.API_URL + 'cdata/request',
                             data={'sessionID': self.cookie_id, 'appid': settings.API_KEY, })

    # Returns basic profile information
    def get_profile(self, user_id):
        data = requests.post(settings.API_URL + 'cdata/request',
                             data={'user': user_id, 'sessionID': self.cookie_id, 'appid': settings.API_KEY, })
        response = parse_response(data)
        return response

    # Shorthand methods.
    def get_name(self, user_id):
        data = self.get_profile(user_id)
        return data['forename'] + ' ' + data['surname']

    def get_balance(self, user_id):
        data = self.get_profile(user_id)
        return data['balance']

    def is_child(self, user_id):
        data = self.get_profile(user_id)
        return data['isChild'] == 1
    """
    Children methods
"""

    # Register a parent's child. Will return an error if it can't be done
    def register_child(self, user_id, forename, surname, date_of_birth, username, password):

        data = requests.post(settings.API_URL + 'cdata/registerchild',
                             data={'user': user_id, 'sessionID': self.cookie_id,
                                   'forename': forename, 'surname': surname,
                                   'dob': date_of_birth,
                                   'username': username,
                                   'password': password,
                                   'appid': settings.API_KEY, })
        response = parse_response(data)
        return response

    # Get all children associated with a parent
    def get_children(self, user_id):
        data = requests.post(settings.API_URL + 'cdata/requestchildren',
                             data={'user': user_id, 'sessionID': self.cookie_id,
                                   'appid': settings.API_KEY, })
        response = parse_response(data)
        return response

    """
    Balance / Stash and transfer methods
"""

    # A single transfer function to use for the accounts view
    def balance_stash_transfer(self, user_id, stash_to_balance_amount, balance_to_stash_amount):
        # Initialize dictionary to use in view for errors and/or success.
        response = dict()
        # Check the result of attempted transfers.
        # Even though validation is done server-side, there is no point in calling them with wrong values.
        if balance_to_stash_amount > 0:
            response['balance_to_stash'] = self.balance_to_stash(user_id, balance_to_stash_amount)
        if stash_to_balance_amount > 0:
            response['stash_to_balance'] = self.stash_to_balance(user_id, stash_to_balance_amount)
        return response

    # Transfer methods
    def stash_to_balance(self, user_id, transfer_amount):

        data = requests.post(settings.API_URL + 'cdata/stashtobalance',
                             data={'user': user_id, 'sessionID': self.cookie_id,
                                   'amount': transfer_amount, 'appid': settings.API_KEY, })
        response = parse_response(data)
        return response

    def balance_to_stash(self, user_id, transfer_amount):
        data = requests.post(settings.API_URL + 'cdata/balancetostash',
                             data={'user': user_id, 'sessionID': self.cookie_id,
                                   'amount': transfer_amount, 'appid': settings.API_KEY, })

        response = parse_response(data)
        return response


    # Transfers money from two users
    def transfer_money(self, user_id, target, amount):
        data = requests.post(settings.API_URL + 'cdata/transfermoney', data={'sessionID': self.cookie_id,
                                                                             'user': user_id, 'target': target,
                                                                             'amount': amount,
                                                                             'appid': settings.API_KEY, })
        response = parse_response(data)
        return response

        """
        Goals methods
"""
    # Returns non-completed goals
    def get_goals(self, user_id):
        data = requests.post(settings.API_URL + 'goals/load', data={'sessionID': self.cookie_id,
                                                                    'user': user_id, 'appid': settings.API_KEY, })
        response = parse_response(data)
        return response

    # Returns all goals
    def get_allgoals(self, user_id):
        data = requests.post(settings.API_URL + 'goals/loadall', data={'sessionID': self.cookie_id,
                                                                       'user': user_id, 'appid': settings.API_KEY, })
        response = parse_response(data)
        return response

    # Completes a goal
    def complete_goal(self, user_id, goal_id):
        data = requests.post(settings.API_URL + 'goals/load', data={'sessionID': self.cookie_id,
                                                                    'user': user_id, 'appid': settings.API_KEY, })
        response = parse_response(data)
        return response

    def create_goal(self, user_id, target_id, desc, amount):

        data = requests.post(settings.API_URL + 'goals/create', data={'sessionID': self.cookie_id,
                                                                      'user': user_id, 'target': target_id,
                                                                      'description': desc, 'amount': amount,
                                                                      'appid': settings.API_KEY, })
        response = parse_response(data)
        return response
    """
        Cards and bonuses
"""
    def get_cards(self, user_id):
        # Values are hardcoded as actual trading cards ould require confirmation and active participation on the part of Lloyds Bank
        response = {'1': {'desc': 'Super Saver', 'date': '16/03/2014'},
                    '2': {'desc': 'Three Goals in a Week', 'date': '26/05/2014'},
                    '3': {'desc': 'Custom Goal Master', 'date': '03/07/2014'}}
        return response

    def get_lloyds_bonuses(self,user_id):
         # Values are hardcoded as actual trading cards ould require confirmation and active participation on the part of Lloyds Bank
        response = {'1': {'desc': 'Toys R Us Voucher', 'date': '18/04/2014'},
                    '2': {'desc': 'Disneyland Paris Discount', 'date': '27/09/2014'}}
        return response
    """
    ATM methods
"""
    def get_atms(self, user_id):
        data = requests.post(settings.API_URL + 'atms/load', data={'sessionID': self.cookie_id,
                                                                   'user': user_id, 'appid': settings.API_KEY, })
        response = parse_response(data)
        return response

    def delete_atm(self, user_id, location_id):
        data = requests.post(settings.API_URL + 'atms/delete', data={'sessionID': self.cookie_id,
                                                                   'user': user_id, 'location':location_id, 'appid': settings.API_KEY, })

        response = parse_response(data)
        return response

    def add_atm(self, user_id, target_id, location_id):
        data = requests.post(settings.API_URL + 'atms/delete', data={'sessionID': self.cookie_id,
                                                                   'user': user_id, 'location':location_id, 'appid': settings.API_KEY, })
        response = parse_response(data)
        return response

# Helper method to automatically parse a received response
def parse_response(data):
    if data.status_code != 200:
        return data.status_code
    else:
        response = data.json()
        if isinstance(response, dict) and 'data' in response:
            return response['data']
        else:
            return str(response)


def not_found_error():
    return {'Status': 'Error',
            'Error': '404', }


def login_error():
    return {'Status': 'Error',
            'Error': '403', }


def server_error():
    return {'Status': 'Error',
            'Error': '500', }