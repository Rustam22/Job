from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from .forms import RegistrationForm

# Create your views here.

def base(request):
    html = render_to_string('accounts/userForm.html', {}, request)
    return HttpResponse(html)


def logout(request):
    context = {}
    html = render_to_string('accounts/logout.html', context, request)
    return HttpResponse(html)


def register(request):
    context = {}
    context['requestData'] = request
    context['requestPostData'] = request.POST

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            #form.save()
            return HttpResponse(render_to_string('accounts/register.html', context, request))
    else:
        form = RegistrationForm()
        context['form'] = form
        return HttpResponse(render_to_string('accounts/register.html', context, request))




"--------------------Registration functions--------------------"

def userForm(request):

    numbers = [1, 2, 3, 4, 5]
    context = {
        'name': 'Rustam',
        'numbers': numbers,
        'template_login': login,
    }

    html = render_to_string('accounts/userForm.html', context, request)
    return HttpResponse(html)

def registration(request):
    context = {'requestData': request, 'requestPostData': request.POST}

    return HttpResponse(render_to_string('accounts/userForm.html', context, request))