from django.db import models
from django.contrib.auth.models import User
import uuid
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    username = models.CharField(max_length=100,blank=True,null=True)
    name = models.CharField(max_length=350,blank=True)
    bio = models.TextField(max_length=1000,blank=True)
    email = models.CharField(max_length=200,blank=False,null=False)
    profile_image = models.ImageField(default='avator.png',upload_to='profile-images/')
    following = models.ManyToManyField(User,related_name='following',blank=True)
    social_instagram = models.CharField(max_length=200,blank=True,null=True)
    social_twitter = models.CharField(max_length=200,blank=True,null=True)
    social_youtube = models.CharField(max_length=200,blank=True,null=True)
    is_verified = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4,unique=True,editable=False,primary_key=True)

    def __str__(self):
        return str(self.user)