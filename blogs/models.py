from django.db import models
import uuid
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
# Create your models here.

class Blog(models.Model):
    BLOG_GENRE = (
        ('Anime','Anime'),
        ('Manga','Manga'),
        ('Webtoon','Webtoon'),
        ('Manhwa','Manhwa'),
        ('Manhua','Manhua'),
    )
    creator = models.ForeignKey(User,on_delete=models.CASCADE,blank=False,null=True)
    title = models.CharField(max_length=500,blank=False,null=True)
    description = RichTextField(blank=True,null=True)
    # description = models.TextField(max_length=5000,blank=True,null=True)
    blog_genre =models.CharField(max_length=100,choices=BLOG_GENRE,null=True)
    tag = models.ManyToManyField('Tag',blank=True)
    blog_thumbnail = models.ImageField(upload_to='blog-thumbnail/',null=True,blank=True)
    blog_image = models.ImageField(default='demo.jpeg',upload_to='blog-images/')
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)
    # upvotes
    
    def __str__(self):
        if self.title == None:
            return "unknown"
        return self.title
        

class Tag(models.Model):
    name = models.CharField(max_length=150,blank=False,null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4,primary_key=True,unique=True,editable=False)

    def __str__(self):
        return str(self.name)

class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=False,null=True)
    blog = models.ForeignKey(Blog,on_delete=models.CASCADE,blank=False,null=True)
    message = models.TextField(max_length=200,blank=True,null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)

    def __str__(self):
        return str(self.message) +' | '+ str(self.user)

    class Meta:
        ordering = ['-created']

