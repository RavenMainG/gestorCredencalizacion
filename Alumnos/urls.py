from django.urls import path
from . import views

urlpatterns = [
    path('panel_alumnos', views.Panel_alumnos, name='panel_alumnos'),
    path('perfil_alumno', views.Perfil_alumnos, name='perfil_alumno'),
    path('cambiar_password', views.Cambiar_password, name='cambiar_password'),
    path('panel_solicitudes', views.Solicitudes_Alumnos, name='panel_solicitudes'),
]