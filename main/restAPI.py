import requests
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
        data = requests.post(settings.API_URL, data={'user':userID, 'appid': settings.API_KEY}) 
        print('profile get!')
        return data.json()['data']



    def get_name(self):
        """
        TODO get userName with cookie/session ID
        """
        return "FirstName LastName"

    def get_balance(self):
        """
        TODO get account balance with cookie/session ID
        """
        return 1000

    def get_stash(self):

        return 1000

    def transfer(self):
        """
        TODO IMPLEMENT
        """


