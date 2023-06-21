from django.urls import path, include
from . import views
from Administradores import urls as administradores_urls
from Alumnos import views as alumnos_views


urlpatterns = [
    path('login_alumnos/', views.login_alumnos, name='login_alumnos'),
    path('logout_alumnos', views.logout_alumnos, name='logout_alumnos'),
    path('registro_alumnos', views.registro_alumnos, name='registro_alumnos'),
    path('', include(administradores_urls)),

    path('registro_administrador/', views.registra_admin, name='registro_administrador'),

    # Rutas para el administrador
    path('login_administrador', views.Login_admin, name='login_administrador'),

    path('qr/<str:matricula>', views.Qr, name='qr'),
    path('panel_alumnos/', alumnos_views.Panel_alumnos, name='panel_alumnos'),
    path('perfil_alumno/', alumnos_views.Perfil_alumnos, name='perfil_alumno'),
    path('cambiar_password/', alumnos_views.Cambiar_password, name='cambiar_password'),
    path('panel_solicitudes_alumnos/', alumnos_views.Solicitudes_Alumnos, name='panel_solicitudes'),

    path('ficha_medica/', alumnos_views.Ficha_medica, name='ficha_medica'),

    path('ruta_qr_alumno/<str:matricula>', alumnos_views.Ruta_qr_alumno, name='ruta_qr_alumno'),

    path('generar_pdf/<str:matricula>', alumnos_views.Generar_credencial_pdf, name='generar_pdf'),

    path('credencial/', alumnos_views.Credencial_pdf, name='credencial'),

    path('gen_pdf/<str:matricula>', views.Gen_pdf, name='gen_pdf'),
]