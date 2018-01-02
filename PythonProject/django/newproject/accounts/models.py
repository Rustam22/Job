from django.db import models
from datetime import datetime
from django.contrib.auth.models import User, AbstractBaseUser
from django import forms
from django.db.models.signals import post_save


# Create your models here.

'''
class UserProfileing(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    firstName = models.CharField(max_length=154, default='')
    lastName = models.CharField(max_length=254, default='')
    email = models.EmailField(max_length=354)
    password = models.CharField(max_length=32)
    date = models.DateTimeField(default=datetime.now, blank=True) 
'''


"--------------------Registration models--------------------"
class UserForm(AbstractBaseUser):

    USERNAME_FIELD = 'username'
    username = models.CharField(max_length=154, default='', db_column='username')
    surname = models.CharField(max_length=254, default='', db_column='surname')
    email = models.EmailField(max_length=354, db_column='email')
    password = models.CharField(max_length=554, db_column='password')
    date = models.DateTimeField(default=datetime.now, blank=True)


