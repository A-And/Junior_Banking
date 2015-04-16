import requests
import logging
from django.conf import settings

__author__ = 'Andon'


class restAPI:

    cookie_id = ""

    def __init__(self, cookie_id):
        """
        TODO get REST connection
        """
        self.cookie_id = cookie_id

    def get_profile(self, user_id):
        print('getting profile..')
        data = requests.post(settings.API_URL + 'cdata/request', data={'user':user_id,'sessionID':self.cookie_id, 'appid': settings.API_KEY, })
        print('profile get!')
        print(data)
        response = parse_response(data)
        return response

    def get_name(self, user_id):
        data = self.get_profile(user_id)
        return data['forename'] + ' ' + data['surname']

    def get_balance(self, user_id):
        data = self.get_profile(user_id)
        return data['balance']

    def transfer(self, sender_id, target_id, amount):
        data = requests.post(settings.API_URL + 'cdata/transfermoney', data={'user':sender_id,'sessionID':self.cookie_id,
                                                                             'target':target_id, 'amount':amount,
                                                                             'appid': settings.API_KEY, })
        response = parse_response(data)
        return response

    def register_child(self, user_id, forename, surname, date_of_birth,):

        data = requests.post(settings.API_URL + 'cdata/registerchild', data={'user':user_id,'sessionID':self.cookie_id,
                                                                             'forename':forename, 'surname':surname,
                                                                             'dob': date_of_birth,
                                                                             'appid': settings.API_KEY, })
        response = data.json()
        if 'Error' in response:
            return {
                'Status': 'Error',
                'Error': response['Error'], }
        else:
            response['Status'] = 'Success'
            return response

    def get_children(self, user_id):
        data = requests.post(settings.API_URL + 'cdata/requestchildren', data={'user':user_id,'sessionID':self.cookie_id,
                                                                               'appid': settings.API_KEY, })
        response = parse_response(data)
        return response

    # A single function to use for the accounts view
    def balance_stash_transfer(self, user_id, balance_to_stash_amount, stash_to_balance_amount):
        # Initialize dictionary to use in view for errors and/or success.
        response = dict()
        # Check the result of attempted transfers
        if balance_to_stash_amount > 0:
            response['balance_to_stash'] = self.balance_to_stash(user_id, balance_to_stash_amount)
        elif balance_to_stash_amount < 0:
            response['balance_to_stash'] = 'Please enter a valid amount'
        if stash_to_balance_amount > 0:
            response['stash_to_balance'] = self.stash_to_balance(user_id, stash_to_balance_amount)

        elif stash_to_balance_amount < 0:
            response['stash_to_balance'] = 'Please enter a valid amount.'
        print(response)
        return response

    def stash_to_balance(self, user_id, transfer_amount):

            data = requests.post(settings.API_URL + 'cdata/stashtobalance', data={'user':user_id,'sessionID':self.cookie_id,
                                                                                   'amount':transfer_amount, 'appid': settings.API_KEY, })
            response = parse_response(data)
            print('Stash to balance response: ')
            print(response)
            return response

    def balance_to_stash(self, user_id, transfer_amount):
        print(transfer_amount)
        data = requests.post(settings.API_URL + 'cdata/balancetostash', data={'user':user_id,'sessionID':self.cookie_id,
                                                                               'amount':transfer_amount, 'appid': settings.API_KEY, })

        response = parse_response(data)
        print('Balance to stash response: ')
        print(response)
        return response

    def logout(self):
        data = requests.post(settings.API_URL + 'cdata/logout', data={'sessionID': self.cookie_id,
                                                                               'appid': settings.API_KEY,})

    def get_goals(self, user_id):
        data = requests.post(settings.API_URL + 'goals/load', data={'sessionID': self.cookie_id,
                                                                          'user':user_id, 'appid': settings.API_KEY, })
        response = parse_response(data)
        return response



def parse_response(data):
    print('DATA GOTTEN IS ' + str(data))
    if data.status_code == 404:
        return 404
    elif data.status_code == 403:
        return 403
    elif data.status_code == 500:
        print('YEAAAAAAAAAAAAAAAAAAAAAAH')
        return 500
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