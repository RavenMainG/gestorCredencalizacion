from django.urls import path
from . import views

urlpatterns = [
    path('panel_solicitudes/', views.PanelAdministradores, name='panel_solicitudes_administrador'),
    path('listado_alumnos/', views.Listado_alumnos, name='listado_alumnos'),
    path('detalle_alumno/<str:matricula>', views.Detalle_alumno, name='detalle_alumno'),
    path('aceptar_solicitud/<str:matricula>', views.Aceptar_solicitud, name='aceptar_solicitud'),
    path('rechazar_solicitud/<str:matricula>', views.Rechazar_solicitud, name='rechazar_matricula'),
    path('editar_alumno/<str:matricula>', views.Editar_alumno, name='editar_alumno'),
    path('desactivar_credencial/<str:matricula>', views.Desactivar_credencial, name='desactivar_credencial'),
    path('eliminar_alumno/<str:matricula>', views.Eliminar_alumno, name='eliminar_alumno'),
]