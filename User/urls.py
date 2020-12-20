from django.urls import path
from . import views

urlpatterns = [
    path('', views.userDashboard, name='userdashboard'),
    path('CourseIntro/', views.userCourseIntro, name="courseIntro"),
    path('CourseLesson/', views.userCourseLesson, name="courseLesson"),
    path('userProfile/', views.userprofile, name='userprofile'),
    path('userProfileEdit/', views.userProfileEdit, name='userprofileedit'),
    path('userCFP/', views.userCfp, name="usercfp"),
    path('userQuizz/<int:w_id>/', views.userQuizz, name="userquizz"),

]
