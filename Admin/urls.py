from django.urls import path
from . import views
urlpatterns = [
    path('', views.landing, name='landing'),
    path('userlogin/', views.userLogin, name='login'),
    path('userlogout/', views.user_logout, name='logout'),
    path('user-register/', views.userRegister, name='register'),

    # path('csmDashboard/',csmDashboard,name='csmdashboard'),

    path('adminDashboard/',views.adminDashboard,name='admindashboard'),
    path('roleCreation/',views.roleCreation,name='rolecreation'),
    path('cfpCreation/',views.cfpCreation,name='cfpcreation'),
    path('cfpList/',views.cfpList,name='cfplist'),
    path('licenseKey/',views.adminLicenseKey,name="licenseKey"),
]
