from django.contrib.auth.models import AbstractUser
from django.db import models
import json

class User(AbstractUser):
    pass

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

class Follow(models.Model):
    user = models.OneToOneField(User, related_name = "user", on_delete=models.CASCADE) 
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)

