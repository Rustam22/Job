from django.db import models
from datetime import datetime
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)
from django import forms
from django.db.models.signals import post_save

# Create your models here.


"-------------------- New Approach --------------------"


class SiteUserManager(BaseUserManager):
    def create_user(self, email, password=None, get_username=None, get_surname=''):
        if not email:
            raise ValueError("User must have an email address")
        if not password:
            raise ValueError("Users must have a password")
        if not get_surname:
            raise ValueError("User must have a name")

        user_obj = self.model(
            email=self.normalize_email(email)
        )
        user_obj.set_password(password)
        user_obj.username = get_username
        user_obj.surname = get_surname
        user_obj.save(using=self._db)

        return user_obj

    def create_active_user(self, email, password, get_username=None):
        user = self.create_user(
            email,
            password=password,
            get_username=get_username
        )
        user.active = True
        user.save(using=self._db)
        return user

    def create_with_barcode(self, email, password, get_username=None):
        user = self.create_user(
            email,
            password=password,
            get_username=get_username
        )
        user.barcode = True
        user.save(using=self._db)
        return user


class SiteUser(AbstractBaseUser):
    username = models.CharField(max_length=154, db_column='username')
    surname = models.CharField(max_length=254, db_column='surname')
    email = models.EmailField(max_length=255, default='abs@mail.com', db_column='email', unique=True)
    active = models.BooleanField(default=True, db_column='active')  # can log in
    barcode = models.BooleanField(default=False, db_column='barcode')  # staff user non super user
    date = models.DateTimeField(auto_now_add=True, db_column='date')

    USERNAME_FIELD = 'email'  # username
    # Username and password are required by default
    REQUIRED_FIELDS = ['']    # surname

    objects = SiteUserManager()

    def __str__(self):     # __unicode__ on Python 2
        return self.email

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_active(self):
        return self.active

    @property
    def is_barcode(self):
        return self.barcode

    @property
    def get_username(self):
        if self.username:
            return self.username
        return self.email

    @property
    def get_surname(self):
        return self.surname

    @property
    def get_date(self):
        return self.date

    @property
    def get_email(self):
        return self.email


#   class UserProfile(models.Model):
#       user = models.OneToOneField(User)


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

<<<<<<< HEAD
def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])

post_save.connect(create_profile, sender=User)
=======
"--------------------Registration models--------------------"
>>>>>>> master



"--------------------Registration models--------------------"

class UserForm(AbstractBaseUser):


"--------------------Registration models--------------------"

class UserForm(models.Model):
    username = models.CharField(max_length=154, default='')
    surname = models.CharField(max_length=254, default='')
    email = models.EmailField(max_length=354)
    password = models.CharField(max_length=554)
    date = models.DateTimeField(default=datetime.now, blank=True)
