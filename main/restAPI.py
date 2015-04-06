__author__ = 'Andon'


class restAPI:

    cookieID = ""

    def __init__(self, cookieID):
        """
        TODO get REST connection
        """
        self.cookieID = cookieID

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


