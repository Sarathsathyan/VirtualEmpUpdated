from django.db import models

from django.contrib.auth.models import User
from Admin.models import (CareerCategory,SubCategory,CategoryCourse)
# Create your models here.

# Career choice
class CareerChoice(models.Model):
    user_id = models.ForeignKey(User,models.CASCADE,null=True)
    cat_id = models.ForeignKey(CareerCategory,models.CASCADE,null=True)
    sub_id = models.ForeignKey(SubCategory,models.CASCADE,null=True)
    cfp_id = models.ForeignKey(CategoryCourse,models.CASCADE,null=True)
