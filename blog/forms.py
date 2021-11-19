from django.contrib.auth import forms
from .models import *
from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.forms import forms
from django.contrib.auth.forms import UserCreationForm
from django import forms

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host']

class register(UserCreationForm):
    email=forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class Profile(ModelForm):
    class Meta:
        model = Imager
        exclude = ['user']



    