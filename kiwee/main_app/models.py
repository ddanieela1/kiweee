from django.db import models
from django.contrib.auth.models import User
import uuid
from datetime import datetime
# # Create your models here.



class Profile(models.Model):
    name = models.CharField(max_length=50)
    profile_image = models.ImageField('profile_imgs', default= 'media/kiwi-default-pic.jpeg')
    about = models.TextField(max_length= 1000, blank = True)
    location = models.TextField(blank = True, max_length= 100)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    id_user = models.IntegerField()

    # show name in admin page
    def __str__(self):
        return self.user.username

class Category(models.Model):
    name = models.CharField(max_length=100, null = False, blank = False)

    def __str__(self):
        return self.name

class Post(models.Model):
    # unique id for post
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    media = models.ImageField(upload_to='posted_media')
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)


    def __str__(self):
        return self.user

