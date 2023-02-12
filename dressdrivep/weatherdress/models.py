from statistics import mode
from django.db import models


class ActivityForm(models.Model):
    MOOD_CHOICES = [
        ("happy", "Happy"),
        ("sad", "Sad"),
        ("excited", "Excited"),
        ("relaxed", "Relaxed"),
        ("energized", "Energized"),
    ]
    mood = models.CharField(max_length=10, choices=MOOD_CHOICES)
    temperature = models.FloatField()

    def __str__(self):
        return self.mood


class Activity(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    mood = models.CharField(max_length=100)
    temperature = models.FloatField()

    def __str__(self):
        return self.name
