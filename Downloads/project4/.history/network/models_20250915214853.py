from django.contrib.auth.models import AbstractUser
from django.db import models
import json

class User(AbstractUser):
    follower = models.IntegerField(default = 0)
    following = models.IntegerField(default = 0)
    def number_of_followers(self):
        return self.follower.count()

class Post(models.Model):
    username = models.CharField()
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.CharField()
    likes = models.ManyToManyField(User, blank = True, related_name="liked" )
    def number_of_likes(self):
        return self.likes.count()

class comment(models.Model):
    cmt_user = models.CharField()
    cmt_timestamp = models.DateTimeField(auto_now_add=True)
    cmt_content = models.CharField()


