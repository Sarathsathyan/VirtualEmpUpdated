from django.db import models
from datetime import datetime
from jsonfield import JSONField
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
    modified = models.DateTimeField(default=datetime.now, null=True) 
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
    xp_points_perq=models.IntegerField(default=0)
    certificate= models.FileField(upload_to="csm_certificates/",null=True)

    # Prerequisite
    requirements=models.TextField(blank=True)
    learnings=models.TextField(blank=True)


    def __str__(self):
        return self.title

class Week(models.Model):
    week_id = models.ForeignKey(Course,on_delete=models.CASCADE)
    week_private = models.CharField(max_length=100,null=True)
    week_name = models.CharField(max_length=100)
    week_date = models.DateTimeField(default=datetime.now,blank=True)

    def __str__(self):
        return  self.week_name

class Week_Unit(models.Model):
    unit_id = models.ForeignKey(Week,on_delete=models.CASCADE)
    unit_caption = models.CharField(max_length=500,null=True)
    unit_video1 = models.FileField(upload_to="Week_Videos/",null=True)
    unit_video2 = models.FileField(upload_to="Week_Videos/",null=True)
    unit_video3 = models.FileField(upload_to="Week_Videos/",null=True)
    u_capThree = models.CharField(max_length=100,null=True, blank=True)
    uCapOne = models.CharField(max_length=150,null=True, blank=True)
    uCap2 = models.CharField(max_length=150,null=True, blank=True)
    video1_duration=models.TimeField(null=True)
    video2_duration=models.TimeField(null=True)
    video3_duration=models.TimeField(null=True)
    def __str__(self):
        return self.unit_caption

class Quizz(models.Model):
    course_id = models.ForeignKey(Course,on_delete=models.CASCADE,null=True)
    week_id = models.ForeignKey(Week,on_delete=models.CASCADE)
    ques_no = models.IntegerField(null=True)
    question = models.CharField(max_length=250)
    option1 = models.CharField(max_length=100)
    option2 = models.CharField(max_length=100)
    option3 = models.CharField(max_length=100)
    option4 = models.CharField(max_length=100)
    option = JSONField(null=True,)
    answer = models.CharField(max_length=100)
    option_available = models.BooleanField(default=False,null=True)

    def __str__(self):
        return self.question

class Result(models.Model):
    result = JSONField()
    score = models.CharField(max_length=100)
    timetaken = models.CharField(max_length=100,null=True)
    user_answer = JSONField()
    auth = models.ForeignKey('auth.User', on_delete=models.CASCADE, )


    class Meta:
        db_table = 'results'

