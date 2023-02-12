from statistics import mode
from django.db import models
from django import forms

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
