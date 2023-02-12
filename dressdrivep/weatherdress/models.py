from atexit import register
import datetime
from distutils.command.upload import upload
from hashlib import blake2b
from pyexpat import model
from statistics import mode
from tabnanny import verbose
from tkinter import CASCADE
from django.db import models
from django import forms
from django.contrib.auth.models import User
from django import template
from pytz import timezone
from django.utils.timesince import timesince


def user_directory_path(instance, filename):
    return "user_{0}/{1}".format(instance.postor.id, filename)

MOOD_CHOICES = [
    ("happy", "Happy"),
    ("sad", "Sad"),
    ("excited", "Excited"),
    ("relaxed", "Relaxed"),
    ("energized", "Energized"),
]


class ActivityForm(forms.Form):
    # mood = models.CharField(max_length=10, choices=MOOD_CHOICES)
    # temperature = models.IntegerField()
    mood_today = forms.CharField(
        label="How are you feeling today?", widget=forms.Select(choices=MOOD_CHOICES)
    )

    def __str__(self):
        return self.mood

class Profile(models.Model):
    user = models.OneToOneField(User, related_name="user", on_delete=models.CASCADE)
    display_name = models.CharField(max_length=25, blank=True, default="User")
    bio  = models.TextField(default="", blank=True)
    email = models.EmailField(default="")
    profile_image   = models.ImageField(null=True, blank=True)
    

class Post(models.Model):
    postor  = models.ForeignKey(Profile, on_delete=models.CASCADE)
    image   = models.ImageField(upload_to=user_directory_path, verbose_name="Image", null=True)
    posts   = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    likes   = models.ManyToManyField(User, blank=True, related_name="likes")
    dislikes = models.ManyToManyField(User, blank=True, related_name="dislikes")

    register = template.Library()
    @register.filter
    def date_posted(self, time_posted):
        timenow  = datetime.datetime.now(timezone.utc)
        try:
            diff = timenow - time_posted
        except:
            return time_posted

        if diff <= datetime.timedelta(minutes=1):
            return "now"
        return "%(time)s ago" % {"time": timesince(time_posted).split(", ")[0]}
    def get_timestamp(self):
        return self.date_posted(self.created)

    @property
    def likes_count(self):
        return self.likes.all().count()

    @property
    def dislikes_count(self):
        return self.dislikes.all().count()

    class Meta:
        verbose_name_plural = "Stories"

    
class Follow(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    following = models.ManyToManyField(User, related_name="follwoing")
    follower   = models.ManyToManyField(User, related_name="follower")

    @classmethod
    def followUser(cls, user, other_user):
        follow_obj = Follow.objects.get(user = user)
        follow_obj.following.add(other_user)

    @classmethod
    def unfollowerUser(cls, user, other_user):
        follow_obj = Follow.objects.get(user = user)
        follow_obj.following.remove(other_user)

    def __str__(self):
        return f'{self.user.username}'

CHOICES = [
    ('like', 'Like'),
    ('unlike', 'Unlike'),
]

class Like(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(choices=CHOICES)
    

    def __str__(self):
        return f"{self.user}-{self.post}-{self.value}"


class Timeline(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    list = models.ManyToManyField(Post, related_name="post_list")
    