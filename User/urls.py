from django.urls import path
from . import views

urlpatterns = [
    path('userdashboard/', views.userDashboard, name='userdashboard'),
    #path('', views.userDashboard, name='userdashboard'),
    path('CourseIntro/<int:course_id>/', views.userCourseIntro, name="courseIntro"),
    path('CourseLesson/<int:c_id>', views.userCourseLesson, name="courseLesson"),
    path('userProfile/', views.userprofile, name='userprofile'),
    path('userProfileEdit/', views.userProfileEdit, name='userprofileedit'),
    path('userCFP/', views.userCfp, name="usercfp"),
    path('userQuizz/<int:w_id>/', views.userQuizz, name="userquizz"),
    path('user_blog_page/',views.user_blog_page,name='user_blog_page'),
    path('userblogsdetail/<int:id>',views.userblogsdetail,name='userblogsdetail'),
    path('displayOnlineCourse/<int:id>',views.displayOnlineCourse,name='displayOnlineCourse'),


    path('userResult/', views.userResult, name="userResult"),
    path('userProject/', views.userProjects, name="userprojects"),
    path('userProjectDesc/', views.userProjectsDesc, name="userprojectsDesc"),
    path('userResult/<int:w_id>/', views.userResult, name="userResult"),
    path('unlockNext/<int:w_id>/', views.unlock, name="unlockNext"),
    path('pricing/', views.pricing, name="pricing"),
    path('license_generate/',views.license_generate,name='license_generate'),
    path('license_page/',views.license_page,name='license_page'),



    path('major_project_dashboard/',views.major_project_dashboard,name='major_project_dashboard'),
]
