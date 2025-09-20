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
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE) #người bấm theo dõi
    following = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE) #người được theo dõi
    class Meta:
        unique_together = ('follower', 'following') #đảm bảo 1 user ko thể follow cùng 1 người nhiều lần
    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"
    def following_list(self):
        return json.dumps([follow.following.username for follow in self.follower.following.all()])


