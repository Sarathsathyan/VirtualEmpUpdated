from django.urls import path
from . import views

urlpatterns =[
    path('',views.userDashboard,name='userdashboard'),
    path('userProfile/',views.userprofile,name='userprofile'),
    path('userProfileEdit/',views.userProfileEdit,name='userprofileedit'),
    path('userCFP/',views.userCfp,name="usercfp"),
    path('userResult/',views.userResult,name="userResult"),

]
