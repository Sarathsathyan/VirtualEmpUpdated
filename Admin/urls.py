from django.urls import path
from . import views
from User.views import userDashboard,userCfp,userprofile,userProfileEdit
from User.views import csmDashboard
urlpatterns = [
    path('', views.landing, name='landing'),
    path('userlogin/', views.userLogin, name='login'),
    path('userlogout/', views.user_logout, name='logout'),
    path('user-register/', views.userRegister, name='register'),

    path('userDashboard/',userDashboard,name='userdashboard'),
    path('userProfile/',userprofile,name='userprofile'),
    path('userProfileEdit/',userProfileEdit,name='userprofileedit'),
    path('userCFP/',userCfp,name="usercfp"),
    path('csmDashboard/',csmDashboard,name='csmdashboard'),

    path('adminDashboard/',views.adminDashboard,name='admindashboard'),
    path('roleCreation/',views.roleCreation,name='rolecreation'),
    path('cfpCreation/',views.cfpCreation,name='cfpcreation'),
    path('cfpList/',views.cfpList,name='cfplist'),
]
