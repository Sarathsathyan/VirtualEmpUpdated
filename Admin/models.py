from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class UserDetails(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    user_phone = PhoneNumberField(null=False, blank=False, unique=False, default='+91')
    user_pass = models.CharField(max_length=10, blank=True)
    user_unique = models.CharField(max_length=100,null=True)
    user_date = models.DateTimeField(default=datetime.now,null=True)
    user_license = models.CharField(max_length=100,null=True)
    user_cfp = models.BooleanField(default=False,blank=True)
    user_workTokens = models.IntegerField()
    user_mcCredits = models.IntegerField()

    def __str__(self):
        return str(self.user_id) if self.user_id else ''




class Reference(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    ref_id = models.CharField(max_length=200)
    used_peoples = models.IntegerField(default=0,null=True)
    used_id = models.CharField(max_length=10,null=True)

class RoleDetail(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    role_user_id=models.CharField(max_length=10)
    user_role=models.CharField(max_length=255)
    role_user_name=models.CharField(max_length=255)
    role_user_email=models.CharField(max_length=255)
    role_user_password=models.CharField(max_length=255)
    role_create_date=models.DateTimeField(default=datetime.now,blank=True)

    def __str__(self):
        return self.role_user_name

class CareerCategory(models.Model):
    category_id=models.IntegerField(default=0)
    category=models.CharField(max_length=255)
    
    def __str__(self):
        return self.category
    """
    def __str__(self):
        return f"pk: {self.pk} category_id: {self.category_id}: {self.category}"
    """
class SubCategory(models.Model):
    cat_id=models.ForeignKey(CareerCategory,on_delete=models.CASCADE)
    sub_category=models.CharField(max_length=255)
    create_date=models.DateTimeField(default=datetime.now)
    
    def __str__(self):
        return self.sub_category
    """
    def __str__(self):
        return f"pk: {self.pk}, cat_id: {self.cat_id}, sub_category: {self.sub_category}, create_date: {self.create_date}"
    """

class CategoryCourse(models.Model):
    cat_id = models.ForeignKey(CareerCategory,on_delete=models.CASCADE)
    sub_id = models.ForeignKey(SubCategory,on_delete=models.CASCADE)
    cfp = models.CharField(max_length=200)
    
    def __str__(self):
        return self.cfp
    """
    def __str__(self):
        return f"pk: {self.pk}, cat_id: {self.cat_id}, sub_id: {self.sub_id}, cfp: {self.cfp}"
    """

class AdminLicense(models.Model):
    key = models.CharField(max_length=100)
    numberCfp = models.IntegerField()
    workTokens = models.IntegerField()
    mcCredits = models.IntegerField()
    date = models.DateTimeField(default=datetime.now, null=True)

    def __str__(self):
        return self.key


class UsedLicense(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    u_key = models.CharField(max_length=100)
    u_wt = models.CharField(max_length=100,null=True)
    u_cfp = models.CharField(max_length=100,null=True)
    u_mCredits = models.CharField(max_length=100,null=True)

    u_date = models.DateTimeField(default=datetime.now,null=True)

    def __str__(self):
        return self.u_key