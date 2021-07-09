from django.urls import path
from . import views

urlpatterns =[
    path('',views.csmDashboard,name="csmdashboard"),
    path('choosetype/',views.chooseType,name='chooseType'),
    path('chooseTypeOnline/',views.chooseType,name='chooseTypeOnline'),
    path('csmaddcourse/<int:cat_id>',views.csmAddCourse,name='csmAddCourse'),
    path('csmAddOnlineCourse/<int:cat_id>',views.csmAddOnlineCourse,name='csmAddOnlineCourse'),
    path('addcurriculam/<int:curr_id>',views.csmAddCurriculam,name='csmAddCurriculam'),
    # online add curriculam
    path('onlinecurriculam/<int:curr_id>', views.onlineAddCurriculam, name='onlineAdd'),
    path('editcourse/<int:course_id>',views.csmEdit,name='csmEdit'),
    path('addQuizz/<int:w_id>/', views.csmAddQuizz, name='csmAddQuizz'),
    path('delQuizz/<int:delId>/<int:w_id>', views.csmDeleteQues, name='deleteQues'),
    path('trainee_dashboard/', views.trainee_dashboard, name='trainee_dashboard'),
    path('csmEditOnlineCourse',views.csmEditOnlineCourse,name='csmEditOnlineCourse'),
]
