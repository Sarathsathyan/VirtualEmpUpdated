from django.db import models

from django.contrib.auth.models import User
from Admin.models import (UserDetails,CareerCategory,SubCategory,CategoryCourse)
from CSM.models import Week_Unit,Week, Course
# Create your models here.


# Career choice
class CareerChoice(models.Model):
    #user_id = models.ForeignKey(User,models.CASCADE,null=True)
    user_id = models.ForeignKey(UserDetails,models.CASCADE,null=True)
    cat_id = models.ForeignKey(CareerCategory,models.CASCADE,null=True)
    sub_id = models.ForeignKey(SubCategory,models.CASCADE,null=True)
    cfp_id = models.ForeignKey(CategoryCourse,models.CASCADE,null=True)



class UserContact(models.Model):
    user_id = models.ForeignKey(UserDetails,on_delete=models.CASCADE)
    gender = models.CharField(max_length=50)
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100)
    user_pic = models.ImageField(upload_to='user_profile/', null=True, blank=True)
    user_bio=models.TextField(blank=False,null=True)


    def __str__(self):
        return self.address1

class UserEducation(models.Model):
    user_id = models.ForeignKey(UserDetails,on_delete=models.CASCADE)
    start_month=models.CharField(max_length=100,blank=True)
    start_year=models.IntegerField(blank=True,default=0)
    end_month=models.CharField(max_length=100,blank=True)
    end_year=models.IntegerField( blank=True,default=0)
    institution = models.CharField(max_length=100)
    state = models.CharField(max_length=200)
    degree = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100,blank=True)
    gpa=models.DecimalField( blank=False,default=0,max_digits=4, decimal_places=2)

    def __str__(self):
        return self.degree


class UserWorkExperience(models.Model):
    user_id = models.ForeignKey(UserDetails,on_delete=models.CASCADE)
    start_month=models.CharField(max_length=100,blank=True)
    start_year=models.IntegerField(blank=True,default=0)
    end_month=models.CharField(max_length=100,blank=True)
    end_year=models.IntegerField( blank=True,default=0)
    job_role = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    state = models.CharField(max_length=200)

    def __str__(self):
        return self.job_role


class UserSkill(models.Model):
    user_id = models.ForeignKey(UserDetails,on_delete=models.CASCADE)
    category=models.CharField(max_length=100)
    skill=models.CharField(max_length=100)

    def __str__(self):
        return self.skill

# CSM  MODELS

# start button
class userProgress(models.Model):
    userId = models.ForeignKey(User,on_delete=models.CASCADE)
    course_id = models.ForeignKey(CategoryCourse,on_delete=models.CASCADE)
    weekId = models.ForeignKey(Week,on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    currentTime = models.DateTimeField(null=True)
    endTime = models.DateTimeField(null=True)
    currentWeek = models.IntegerField(default=1,null=True)

    def __str__(self):
        return self.status

# Pricing section
class userPricing(models.Model):
    userId = models.ForeignKey(User,on_delete=models.CASCADE)
    cfpCount = models.IntegerField()
    workTokens = models.IntegerField()
    mcCredits = models.IntegerField()

class pricingSec(models.Model):
    cef = models.IntegerField()
    cfpPrice = models.IntegerField()
    wToken = models.IntegerField()
    mcCredits = models.IntegerField()

    def __str__(self):
        return self.cef

class Score(models.Model):
    userId = models.ForeignKey(User,on_delete=models.CASCADE)
    week_id=models.ForeignKey(Week, on_delete=models.CASCADE)
    #course_id=models.ForeignKey(Course,on_delete=models.CASCADE)
    totalxp=models.IntegerField(default=0)