from django.urls import path
from .views import *


urlpatterns = [
    path('', index, name='register'),
    path('signout', signout_page,name='signout'),
    path('signin', signin_page,name='signin'),
]