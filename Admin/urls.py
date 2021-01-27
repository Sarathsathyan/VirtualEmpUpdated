from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('userlogin/', views.userLogin, name='login'),
    path('userlogout/', views.user_logout, name='logout'),
    path('user-register/', views.userRegister, name='register'),
    path('activatecode/',views.activatecode,name='activatecode'),

    # path('csmDashboard/',csmDashboard,name='csmdashboard'),

    path('adminDashboard/',views.adminDashboard,name='admindashboard'),
    path('roleCreation/',views.roleCreation,name='rolecreation'),
    path('cfpCreation/',views.cfpCreation,name='cfpcreation'),
    path('cfpList/',views.cfpList,name='cfplist'),
    path('categoryEdit/<int:c_id>',views.cateEdit,name='categoryEdit'),
    path('SubcategoryEdit/<int:s_id>',views.subEdit,name='subEdit'),

    path('admindashboard/student_info/', views.adminStudents, name='adminStudents'),
    path('admindashboard/courses/',views.adminCourses,name='admincourse'),
    path('licenseKey/',views.adminLicenseKey,name="licenseKey"),

    path('instructors/',views.viewInstructor,name='instructors'),
    path('delInstructor/<int:dId>/',views.deleteInstructor,name='delInstructor'),

    path('deleteStudent/<int:delId>/',views.deleteStu,name='deleteStudent'),
    path('viewTrainee/<int:userId>/',views.adminViewStudent,name='viewStudent')
]
