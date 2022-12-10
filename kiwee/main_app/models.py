from django.db import models
from django.contrib.auth.models import User
# # Create your models here.


class Profile(models.Model):
    name = models.CharField(max_length=50)
    profile_image = models.ImageField('profile_imgs', default= 'media/kiwi-default-pic.jpeg')
    likes = models.IntegerField()
    about = models.TextField(blank = True, max_length= 1000)
    location = models.TextField(blank = True, max_length= 100)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    id_user = models.IntegerField()

    # show name in admin page

    def __str__(self):
        return self.user.username