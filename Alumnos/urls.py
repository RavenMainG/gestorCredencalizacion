from django.urls import path
from . import views

urlpatterns = [
    path('panel_alumnos/', views.Panel_alumnos, name='panel_alumnos'),
    path('perfil_alumno/', views.Perfil_alumnos, name='perfil_alumno'),
    path('cambiar_password/', views.Cambiar_password, name='cambiar_password'),
    path('panel_solicitudes/', views.Solicitudes_Alumnos, name='panel_solicitudes'),

    path('ficha_medica/', views.Ficha_medica, name='ficha_medica'),

    path('ruta_qr_alumno/<str:matricula>', views.Ruta_qr_alumno, name='ruta_qr_alumno'),

    path('generar_pdf/<str:matricula>', views.Generar_credencial_pdf, name='generar_pdf'),

    path('credencial/', views.Credencial_pdf, name='credencial'),

]