from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.forms import forms



# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    firstName = models.CharField(max_length=154, default='')
    lastName = models.CharField(max_length=254, default='')
    email = models.EmailField(max_length=354)
    password = models.CharField(max_length=32)
    date = models.DateTimeField(default=datetime.now, blank=True)



