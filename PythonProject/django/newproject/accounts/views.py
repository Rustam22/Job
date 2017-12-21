from django.http import HttpResponse
from django.template.loader import render_to_string


# Create your views here.



def login(request):
    html = render_to_string('accounts/login.html', {'name': 'Rustam'}, request)
    return HttpResponse(html)
