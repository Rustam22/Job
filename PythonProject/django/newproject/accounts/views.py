from django.http import HttpResponse
from django.template.loader import render_to_string
from django.template import engines
from django.views.generic.base import TemplateView

# Create your views here.


def login(request):
    html = render_to_string('accounts/login.html', {'name': 'Rustam'}, request)
    return HttpResponse(html)
