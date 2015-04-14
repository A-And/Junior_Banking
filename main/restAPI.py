import requests
import logging
from django.conf import settings

__author__ = 'Andon'


class restAPI:

    cookieID = ""

    def __init__(self, cookieID):
        """
        TODO get REST connection
        """
        self.cookieID = cookieID


    def get_profile(self, userID):
        print('getting profile..')
        data = requests.post(settings.API_URL + 'cdata/request', data={'user':userID,'sessionID':self.cookieID, 'appid': settings.API_KEY, })
        print('profile get!')
        print(data)
        print(settings.API_URL + 'request')
        return data.json()['data']


    def get_name(self, userID):
        data = self.get_profile(userID)
        return data['forename'] + ' ' + data['surname']

    def get_balance(self, userID):
        data = self.get_profile(userID)
        return data['balance']


    def transfer(self, senderID, targetID, amount):
        data = requests.post(settings.API_URL + 'cdata/transfermoney', data={'user':senderID,'sessionID':self.cookieID,
                                                                             'target':targetID, 'amount':amount,
                                                                             'appid': settings.API_KEY, })
        response = data.json()
        if 'Error' in response:
            return {
                'Status': 'Error',
                'Error': response['Error'], }
        else:
            response['Status'] = 'Success'
            return response

    def register_child(self, userID, forename, surname, date_of_birth,):

        data = requests.post(settings.API_URL + 'cdata/registerchild', data={'user':userID,'sessionID':self.cookieID,
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


    def get_children(self, userID):
        data = requests.post(settings.API_URL + 'cdata/requestchildren', data={'user':userID,'sessionID':self.cookieID,
                                                                               'appid': settings.API_KEY, })
        response = data.json()
        if 'Error' in response:
            return {
                'Status': 'Error',
                'Error': response['Error'], }
        else:
            response['Status'] = 'Success'
            return response
    def logout(self):
        data = requests.post(settings.API_URL + 'cdata/requestchildren', data={'sessionID': self.cookieID,
                                                                               'appid': settings.API_KEY, })