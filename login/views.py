from django.shortcuts import render_to_response
from django.template import loader, RequestContext


# Create your views here.
def landing(request):
    return render_to_response("Landing_Page.html", context_instance=RequestContext(request))