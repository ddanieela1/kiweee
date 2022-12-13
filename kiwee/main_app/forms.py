from django import forms
from django.contrib.auth.models import User
from django.db import models
from .models import Venue
from django.forms import ModerlForm



Class SettingsForm(UserCreationForm):

email = forms.EmailField(required=True)
    Class Meta:
    model= User
    fields = ('username', 'password', 'password2' 'email')
  

    def save(save, commit = True):
        user = super(NewUserForm, self).save(commit = False)
        user.email = save.cleaned_data['email']
        if commit:
            user.save()
        return user