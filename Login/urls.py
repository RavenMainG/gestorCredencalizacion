from django.urls import path, include
from . import views
from Alumnos import urls as alumnos_urls

urlpatterns = [
    path('login_alumnos/', views.login_alumnos, name='login_alumnos'),
    path('login_administradores/', views.login_administradores, name='login_administradores'),
    path('registro_alumnos', views.registro_alumnos, name='registro_alumnos'),
    path('panel_alumnos/', include(alumnos_urls)),
]