from django.shortcuts import render, redirect
from Login.models import Alumno
from django.contrib.auth.decorators import login_required

def no_cache(view_func):
    def wrapped_view(*args, **kwargs):
        response = view_func(*args, **kwargs)
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        return response

    return wrapped_view


def buscar_exitencia_solicitudes():



    alumnos = Alumno.objects.all()
    print(alumnos)
    for alumno in alumnos:
        if alumno.solicitud.exists() == True:
            return True
    return False


def buscar_solicitudes_pendientes():



    alumnos = Alumno.objects.all()
    solicitudes = []
    for alumno in alumnos:
        if alumno.estado_solicitud() == 'Pendiente':
            solicitudes.append(alumno)

    return solicitudes


def validar_si_hay_solicitudes_pendientes():
    alumnos = Alumno.objects.all()
    for alumno in alumnos:
        if alumno.solicitud.filter(estado_solicitud='pendiente').exists() == True:
            return True
    return False

def listar_alumnos():
    alumnos = Alumno.objects.all()
    return alumnos


@no_cache
@login_required
def PanelAdministradores(request):

    if request.user.is_superuser == False:
        return redirect('panel_alumnos')

    solicitudes = buscar_solicitudes_pendientes()

    print(solicitudes)
    return render(request, 'Administradores/panel_administrador/panel_solicitudes.html', {'solicitudes': solicitudes})

def Aceptar_solicitud(request, matricula):
    alumno = Alumno.objects.get(matricula=matricula)

    alumno.aceptar_solicitud()
    alumno.activar_credencial_alumno()

    return redirect('panel_solicitudes_administrador')

def Rechazar_solicitud(request, matricula):
    alumno = Alumno.objects.get(matricula=matricula)
    alumno.rechazar_solicitud()

    return redirect('panel_solicitudes_administrador')

@no_cache
@login_required
def Listado_alumnos(request):

    if request.user.is_superuser == False:
        return redirect('panel_alumnos')

    alumnos = listar_alumnos()
    context = {
        'alumnos': alumnos
    }
    return render(request, 'Administradores/listado_alumnos/listado_alumnos.html', context)

@no_cache
@login_required
def Detalle_alumno(request, matricula):


    if request.user.is_superuser == False:
        return redirect('panel_alumnos')

    alumno = Alumno.objects.get(matricula=matricula)

    url = alumno.imagen.url
    nueva_url = url.split('/')
    url = nueva_url[nueva_url.__len__() - 2] + "/" + nueva_url[nueva_url.__len__() - 1]

    context = {
        'alumno': alumno,
        'imagen': url
    }
    return render(request, 'Administradores/detalle_alumno/detalle_alumno.html', context)

def Editar_alumno(request, matricula):

    alumno = Alumno.objects.get(matricula=matricula)

    if request.method == 'POST':
        pass
    else:
        context = {
            'alumno': alumno
        }
        return render(request, 'Administradores/editar_alumno/editar_alumno.html', context)

def Desactivar_credencial(request, matricula):
    alumno = Alumno.objects.get(matricula=matricula)
    alumno.desactivar_credencial_alumno()
    return redirect('listado_alumnos')

def Eliminar_alumno(request, matricula):

    alumno = Alumno.objects.get(matricula=matricula)
    alumno.delete()
    return redirect('listado_alumnos')
