from django.urls import path
from . import views

urlpatterns = [
    path('login_alumnos/', views.login_alumnos, name='login_alumnos'),
    path('login_administradores/', views.login_administradores, name='login_administradores'),
]