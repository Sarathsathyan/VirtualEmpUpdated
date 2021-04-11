from django.urls import path
from . import views

urlpatterns = [
    path('', views.traineeDash, name='traineeDash')
]
