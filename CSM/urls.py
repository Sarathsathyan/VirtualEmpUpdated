from django.urls import path
from . import views

urlpatterns =[
    path('',views.csmDashboard,name="csmdashboard"),
    path('choosetype/',views.chooseType,name='chooseType'),
    path('choosetype/', views.chooseType, name='chooseType'),
    path('csmaddcourse/<int:cat_id>',views.csmAddCourse,name='csmAddCourse'),
]