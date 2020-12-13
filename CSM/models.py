from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
# Create your models here.

CATEGORY_CHOICES = (
    ('IT', 'IT & Software'),
    ('Business & Startups', 'Business & Startups'),
    ('Designing', 'Designing'),
    ('Electronics & Electricals', 'Electronics & Electricals'),
)
DIFFICULTY_LEVEL=(
    ('Beginner', 'Beginner'),
    ('Intermediate', 'Intermediate'),
    ('Advanced', 'Advanced'),
)

class CreateCourse(models.Model):
    create_user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    create_category=models.CharField(max_length=255,null=True)
    create_sub=models.CharField(max_length=255,null=True)
    create_course=models.CharField(max_length=255)
    # create_instructor = models.CharField(max_length=255, null=True)
    create_time=models.DateTimeField(default=datetime.now,blank=True)

    def __str__(self):
        return self.create_category

class Course(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(CreateCourse,on_delete=models.CASCADE,null=True)
    created = models.DateTimeField(default=datetime.now, null=True)
    title = models.CharField(max_length=50)
    tagline=models.CharField(max_length=50)
    short_description=models.CharField(max_length=100)
    course_image=models.ImageField(upload_to='csm_images/',null=True,blank=True)

    difficulty_level=models.CharField(max_length=20, choices=DIFFICULTY_LEVEL,null=True, blank=True)
    instructor=models.CharField(max_length=200,null=True, blank=True)

    # meta section
    meta_keywords=models.TextField(blank=True)
    meta_description=models.TextField(blank=True)

    # rewards
    course_points=models.IntegerField(default=0)
    certificate= models.CharField(max_length=200, null=True, blank=True)

    # Prerequisite
    requirements=models.TextField(blank=True)
    learnings=models.TextField(blank=True)


    def __str__(self):
        return self.title