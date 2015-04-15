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
        print(settings.API_URL + 'request')
        return data.json()['data']

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
        response = data.json()
        if 'Error' in response:
            return {
                'Status': 'Error',
                'Error': response['Error'], }
        else:
            response['Status'] = 'Success'
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
        response = data.json()
        if 'Error' in response:
            return {
                'Status': 'Error',
                'Error': response['Error'], }
        else:
            response['Status'] = 'Success'
            return response

    def balance_stash_transfer(self, user_id, balance_to_stash_amount, stash_to_balance_amount):
        # Initialize dictionary to use in view for errors and/or success.
        response = dict()
        # Check the result of attempted transfers
        if balance_to_stash_amount > 0:
            response['balance_to_stash'] = self.balance_to_stash(user_id, balance_to_stash_amount)
        else:
            response['balance_to_stash'] - 'Please enter a valid amount'
        if stash_to_balance_amount > 0:
            response['stash_to_balance'] = self.stash_to_balance(user_id, stash_to_balance_amount)
        else:
            response['stash_to_balance'] = 'Please enter a valid amount.'

    def stash_to_balance(self, user_id, transfer_amount):
        data = requests.post(settings.API_URL + 'cdata/stashtobalance ', data={'user':user_id,'sessionID':self.cookie_id,
                                                                               'amount':transfer_amount, 'appid': settings.API_KEY, })

        response = data.json()
        if 'Error' in response:
            return {
                'Status': 'Error',
                'Error': response['Error'], }
        else:
            response['Status'] = 'Success'
            return response

    def balance_to_stash(self, user_id, transfer_amount):
        data = requests.post(settings.API_URL + 'cdata/balancetostash ', data={'user':user_id,'sessionID':self.cookie_id,
                                                                               'amount':transfer_amount, 'appid': settings.API_KEY, })

        response = data.json()
        if 'Error' in response:
            return {
                'Status': 'Error',
                'Error': response['Error'], }
        else:
            response['Status'] = 'Success'
            return response

    def logout(self):
        data = requests.post(settings.API_URL + 'cdata/logout', data={'sessionID': self.cookie_id,
                                                                               'appid': settings.API_KEY,})

    def get_goals(self, user_id):
        data = requests.post(settings.API_URL + 'goals/load', data={'sessionID': self.cookie_id,
                                                                          'user':user_id, 'appid': settings.API_KEY, })
        print(data)



def parse_response(self, response):
        if response == '404':
            return not_found_error()
        elif response == '403':
            return login_error()
        else:
            data = response.json()
            if 'Error' in response:
                return {
                    'Status': 'Error',
                    'Error': response['Error'], }
            else:
                response['Status'] = 'Success'
                return response

def not_found_error(self):
    return {'Status': 'Error',
            'Error': '404', }


def login_error(self):
    return {'Status': 'Error',
            'Error': '403', }