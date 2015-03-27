from django.shortcuts import render_to_response, render
from django.template import loader, RequestContext
from login.forms import LoginForm


def landing(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

    else:
        form = LoginForm()

    return render(request, 'Landing_Page.html', {'form': form, })