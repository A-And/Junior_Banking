import urllib.parse
import urllib.request
import logging
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.template import loader, RequestContext
from django.conf import settings
from login.forms import LoginForm


def landing(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        logger = logging.getLogger(__name__)
        if form.is_valid():
            api_url = settings.API_URL

            post_values = {
                'appid': settings.API_KEY,
                'user': form.cleaned_data['email'],
                'password': form.cleaned_data['password']
            }
            logger.debug(post_values)


            post_data = urllib.parse.urlencode(post_values).encode('ascii')
            logger.debug(post_data)
            req = urllib.request.Request(api_url + cdata/request', post_data)
            logger.debug(api_url + 'cdata/request')
            response = urllib.request.urlopen(req)
            page = response.read()
            return HttpResponseRedirect('Landing_Page.html')

    else:
        form = LoginForm()

    return render(request, 'Landing_Page.html', {'form': form, })


