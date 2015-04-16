from django.core.exceptions import PermissionDenied
from django.http import Http404

__author__ = 'Andon'


def validate_response(response):
    if isinstance(response, int):
        if response == 403:
            raise PermissionDenied()
        elif response == 404:
            raise Http404()