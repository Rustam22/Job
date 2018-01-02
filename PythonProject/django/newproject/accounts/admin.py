from django.contrib import admin
from .models import UserProfile, UserForm

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(UserForm)