from django.urls import path
from . import views

urlpatterns = [
    path('',views.major_project_dashboard,name='major_project_dashboard'),
    path('project_creation',views.project_creation,name='project_creation'),
]
