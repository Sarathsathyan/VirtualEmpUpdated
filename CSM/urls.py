from django.urls import path
from . import views

urlpatterns =[
    path('',views.csmDashboard,name="csmdashboard"),
    path('choosetype/',views.chooseType,name='chooseType'),
    path('choosetype/', views.chooseType, name='chooseType'),
    path('csmaddcourse/<int:cat_id>',views.csmAddCourse,name='csmAddCourse'),
    path('addcurriculam/<int:curr_id>',views.csmAddCurriculam,name='csmAddCurriculam'),
    path('editcourse/<int:course_id>',views.csmEdit,name='csmEdit'),
    path('addQuizz/<int:w_id>/', views.csmAddQuizz, name='csmAddQuizz'),
    path('delQuizz/<int:delId>/<int:w_id>', views.csmDeleteQues, name='deleteQues'),
    path('trainee_dashboard/', views.trainee_dashboard, name='trainee_dashboard'),
]
