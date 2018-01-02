from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserForm



class TestRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = {
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        }

    def save(self, commit=True):
        user = super(TestRegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user


# --------------------------------- My registration form --------------------------------- #
class RegistrationFrom(UserCreationForm):
    email = forms.EmailField(required=True)
    username = forms.EmailField(required=True)
    surname = forms.EmailField(required=True)

    class Meta:
        model = UserForm

        fields = ('username', 'surname', 'email', 'password1', 'password2',)

        widgets = {
            'password1': forms.PasswordInput(),
        }

    def save(self, commit=True):
        user = super(RegistrationFrom, self).save(commit=False)
        user.username = self.cleaned_data['username']
        user.surname = self.cleaned_data['surname']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user


class SignUpForm(UserCreationForm):

    class Meta:
        model = UserForm
        fields = ['username', 'surname', 'email', 'password1', 'password2']
        widgets = {
            'password1': forms.PasswordInput(),
        }

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.username = self.cleaned_data['username']
        user.surname = self.cleaned_data['surname']
        user.email = self.cleaned_data['email']
        user.set_password(self.cleaned_data["password1"])


        if commit:
            user.save()

        return user