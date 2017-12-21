from django.http import HttpResponse
from django.template.loader import render_to_string


# Create your views here.

def base(request):
    html = render_to_string('accounts/base.html', {}, request)
    return HttpResponse(html)


def login(request):

    numbers = [1, 2, 3, 4, 5]
    context = {
        'name': 'Rustam',
        'numbers': numbers
    }

    html = render_to_string('accounts/login.html', context, request)
    return HttpResponse(html)


