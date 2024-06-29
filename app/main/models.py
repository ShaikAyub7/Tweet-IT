from django.db import models
from django.utils.text import slugify
import uuid
import datetime
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings

# Create your models here.

class Tweet(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField(max_length=240)
    photo = models.ImageField(upload_to='photos/',null=True,blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(User, related_name='liked_tweets', blank=True)

    def __str__(self) -> str:
        return f'{self.user.username} - {self.text[:10]}'
        
    def total_likes(self):
        return self.likes.count()
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    # Add any other fields you want for the profile


class Reply(models.Model):
    tweet = models.ForeignKey(Tweet, related_name='replies', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.CharField(max_length=240)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text
    


