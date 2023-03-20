from django.urls import path, include
from . import views
from Alumnos import urls as alumnos_urls
from Administradores import urls as administradores_urls

urlpatterns = [
    path('login_alumnos/', views.login_alumnos, name='login_alumnos'),
    path('logout_alumnos', views.logout_alumnos, name='logout_alumnos'),
    path('registro_alumnos', views.registro_alumnos, name='registro_alumnos'),

    path('panel_alumnos/', include(alumnos_urls)),
    path('panel_administrador/', include(administradores_urls)),

    path('registro_administrador', views.registra_admin, name='registro_administrador'),

    # Rutas para el administrador
    path('login_administrador', views.Login_admin, name='login_administrador'),

    path('qr/<str:matricula>', views.Qr, name='qr')
]