from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    email = models.TextField(max_length=524)
    password = models.TextField(max_length=254)
    age = models.IntegerField()


