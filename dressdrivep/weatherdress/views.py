from urllib.parse import urlencode
from wsgiref.util import request_uri
from django.http import request, response
from django.shortcuts import render
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, logout, authenticate
from urllib.request import urlopen
import requests
import googlemaps
from geopy.geocoders import Nominatim
from .forms import *
from django.contrib.auth.models import User
import numpy as np
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from django.shortcuts import render
from .models import ActivityForm


def index(request):
    context = {}
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]
            try:
                User.objects.get(email=email)
                error = "E-mail already registered!"
                context["error"] = error
                context["form"] = form
                return render(request, "weatherdress/registration.html", context)
            except User.DoesNotExist:
                username = form.cleaned_data["username"]
                first_name = form.cleaned_data["first_name"]
                last_name = form.cleaned_data["last_name"]
                password = form.cleaned_data["password"]
                user = User(
                    username=username,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                )
                user.set_password(password)
                user.save()
                login(request, user)
                return redirect("home")

        else:
            return render(request, "weatherdress/registration.html", {"form": form})

    form = UserRegistrationForm()
    context["form"] = form

    return render(request, "weatherdress/registration.html", context)


def signout_page(request):
    # tl   = TimeLine.objects.get(owner=request.user.profile)
    # stringed = str(tl)
    # listed = stringed.split(" ")
    # dictionary = dict()
    # dictionary['displayname'] = listed[0]
    logout(request)
    return render(request, "bros/signout.html")


def signin_page(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        # set requirements (parameters) for authentication
        user = authenticate(username=username, password=password)

        # if authenticated go home
        if user:
            login(request, user)
            return redirect("home")

    form = UserLoginForm()
    context = {
        "form": form,
    }
    return render(request, "weatherdress/signin.html", context)


def home(request):
    API_KEY = open("apikey.txt", "r").read()
    ip_request = requests.get("https://get.geojs.io/v1/ip.json")
    my_ip = ip_request.json()["ip"]
    geo_request = requests.get(f"https://get.geojs.io/v1/ip/geo/{my_ip}.json")
    geo_data = geo_request.json()
    latitude = geo_data["latitude"]
    longitude = geo_data["longitude"]

    request_url = "https://api.openweathermap.org/data/3.0/onecall?lat={latitude}&lon={longitude}&appid={API_KEY}"
    response = requests.get(request_url).json()


def recommend_activity(mood):
    # Define a list of activities and their corresponding moods
    activities = ["outdoor sports", "dancing", "meditation", "yoga", "reading"]
    moods = ["energetic", "happy", "relaxed", "calm", "calm"]

    # Convert the list of activities and moods into a matrix representation
    X = np.array([activities, moods])
    y = np.array(moods)

    # Train a Naive Bayes classifier on the matrix representation
    clf = MultinomialNB()
    clf.fit(X, y)

    # Use the trained classifier to predict the recommended activity based on the user's mood
    mood_vector = np.array([mood])
    return clf.predict(mood_vector)


def recommend_activity_view(request):
    if request.method == "POST":
        mood = request.POST.get("mood")
        activity = recommend_activity(mood)
        return render(request, "recommend_activity.html", {"activity": activity})
    else:
        return render(request, "input_mood.html")


def activity_form_view(request):
    form = ActivityForm()
    return render(request, "activity_form.html", {"form": form})
