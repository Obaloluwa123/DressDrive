from distutils.command.upload import upload
from hashlib import blake2b
from statistics import mode
from tkinter import CASCADE
from django.db import models
from django import forms
from django.contrib.auth.models import User


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