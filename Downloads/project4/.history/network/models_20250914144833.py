from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    username = models.CharField()
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.CharField()
    likes = models.IntegerField()
