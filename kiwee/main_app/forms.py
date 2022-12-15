from django import forms
from django.contrib.auth.models import User
from django.db import models
from . models import Post
from django.forms import ModelForm



class UploadForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['media','caption', 'user' ]
