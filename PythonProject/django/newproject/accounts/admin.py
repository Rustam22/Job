from django.contrib import admin
from .models import (
    UserForm, User
)

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(UserForm)