from django import forms
from django.db import models
from . models import Post
from django.forms import ModelForm



class PostForm(forms.ModelForm):
   class Meta:
     model = Post
     fields = '__all__'

     