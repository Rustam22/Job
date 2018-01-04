from django.contrib import admin
from .models import (
    UserForm, SiteUser
)

# Register your models here.
admin.site.register(UserForm)
admin.site.register(SiteUser)