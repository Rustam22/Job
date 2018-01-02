from django.http import HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

from .forms import TestRegistrationForm, UserForm, RegistrationFrom, SignUpForm

# Create your views here.

# --------------------------------- My registration form --------------------------------- #
def base(request):
    html = render_to_string('accounts/userForm.html', {'status': 'registration'}, request)
    return HttpResponse(html)


def signup(request):
    context = {'requestData': request, 'requestPostData': request.POST}

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            context['status'] = 'login'
            context['form'] = form
            context['formV'] = form.is_valid()
            form.save()

            return HttpResponse(render_to_string('accounts/userForm.html', context, request))

        else:
            context['status'] = 'registration'
            context['form'] = form
            context['formV'] = form.is_valid()
            return HttpResponse(render_to_string('accounts/userForm.html', context, request))