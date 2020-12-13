from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
# Create your models here.

class BlogManager(models.Model):
     user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
     blog_title=models.CharField(max_length=100)
     blog_tagline=models.CharField(max_length=150,blank=True)
     blog_body=models.TextField(blank=True)
     blog_thumbnail=models.ImageField(upload_to='blog_images/',null=True,blank=True)
     blog_category=models.CharField(max_length=200,null=True, blank=True)
     blog_date = models.DateTimeField(default=datetime.now,blank=True)

     def __str__(self):
         return self.blog_title


class BlogHeight(models.Model):
     user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
     blog_title = models.CharField(max_length=100)
     blog_body = models.TextField(blank=True)
     blog_thumbnail = models.ImageField(upload_to='blog_highlight/', null=True, blank=True)
     blog_date = models.DateTimeField(default=datetime.now, blank=True)

     def __str__(self):
         return self.blog_title


class BlogCategory(models.Model):
     blog_category_id=models.IntegerField(default=0)
     blog_category=models.CharField(max_length=255)

     def __str__(self):
         return self.blog_category
