from django.urls import path, include
from . import views
from Alumnos import urls as alumnos_urls

urlpatterns = [
    path('login_alumnos/', views.login_alumnos, name='login_alumnos'),
    path('logout_alumnos', views.logout_alumnos, name='logout_alumnos'),
    path('registro_alumnos', views.registro_alumnos, name='registro_alumnos'),
    path('panel_alumnos/', include(alumnos_urls)),
]