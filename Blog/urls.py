from django.urls import path
from . import views

urlpatterns =[
    path('',views.blogManager,name='blogManager'),
    path('bloghighlight/', views.blogHighlight, name='blogHighlight'),
    path('blogeditmanager/<int:id>',views.blogEditManager,name='blogEditManager'),
    path('blogdashboard/',views.blogDashboard,name='blogDashboard'),
    path('blogcategorycreate/',views.blogcategorycreate,name='blogcategorycreate'),

]
