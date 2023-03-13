from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password, make_password

from Login.models import Alumno, Credencial, Solicitud


def no_cache(view_func):
    def wrapped_view(*args, **kwargs):
        response = view_func(*args, **kwargs)
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        return response

    return wrapped_view

@no_cache
@login_required
def Solicitudes_Alumnos(request):

    alumno = Alumno.objects.get(email=request.user.email)
    credencial = alumno.credencial
    print(credencial)

    if alumno.credencial == None:

        print(alumno.solicitud.all())
        requiere_credencial = True
        context = {
            'title': 'Solicitudes de Alumnos',
            'mensaje': 'No tienes tu credencial aun, realiza una solicitud para poder obtenerla',
            'mensaje_solicitud': 'Se ha enviado tu solicitud, espera a que el administrador te la active',
            'credencial': requiere_credencial
        }

        credencial = Credencial.objects.create(estado_credencial='Inactiva')
        alumno.credencial = credencial

        solicitud = Solicitud.objects.create(tipo_solicitud='Primera credencial', estado_solicitud='Pendiente')
        alumno.solicitud.add(solicitud)

        alumno.save()

        return render(request, 'Alumnos/solicitudes/solicitudes_alunno.html', context)

    else:
        print(alumno.solicitud.all())
        return render(request, 'Alumnos/solicitudes/solicitudes_alunno.html')


@no_cache
@login_required
def Cambiar_password(request):

    if request.method == 'POST':

        alumno = Alumno.objects.get(email=request.user.email)
        print(f'pass1: {alumno.password}')

        password_actual = request.POST['password_actual']
        password_nueva = request.POST['nueva_password']
        password_repeticion = request.POST['repeticion_password']

        if not check_password(password_actual, request.user.password):
            context = {
                'error': 'No has ingresado bien tu contrasena actual'
            }
            return render(request, 'Alumnos/actualizar_password/actualizar_password.html', context)
        else:
            if password_nueva != password_repeticion:
                context = {
                    'error': 'La contrasena nueva no coincide con la repeticion'
                }
                return render(request, 'Alumnos/actualizar_password/actualizar_password.html', context)

            else:
                password_nueva = make_password(password_nueva)
                alumno = Alumno.objects.get(email=request.user.email)
                alumno.password = password_nueva
                alumno.save()
                context = {
                    'mensaje': 'Se actualizado tu contrasena'
                }
                return render(request, 'Alumnos/actualizar_password/actualizar_password.html', context)

    else:
        return render(request, 'Alumnos/actualizar_password/actualizar_password.html')


@no_cache
@login_required
def Perfil_alumnos(request):
    if request.method == 'POST':
        alumno = Alumno.objects.get(email=request.user.email)

        alumno.nombre = request.POST['nombres']
        alumno.apellido = request.POST['apellidos']
        alumno.matricula = request.POST['matricula']
        alumno.numero_telefono = request.POST['numero_telefono']
        alumno.fecha_nacimiento = request.POST['fecha_nacimiento']
        alumno.direccion = request.POST['direccion']
        alumno.email = request.POST['email']
        alumno.save()

        context = {
            'title': 'Perfil de Alumnos',
            'nombre_alumnos': alumno.nombre,
            'apellido_alumnos': alumno.apellido,
            'matricula_alumnos': alumno.matricula,
            'carrera_alumnos': alumno.carrera,
            'cuatrimestre_alumnos': alumno.cuatrimestre,
            'numero_telefono_alumnos': alumno.numero_telefono,
            'fecha_nacimiento_alumnos': alumno.fecha_nacimiento,
            'direccion_alumnos': alumno.direccion,
            'tipo_alumno_alumnos': alumno.tipo_alumno,
            'email_alumnos': alumno.email,
        }

        return render(request, 'Alumnos/perfil/perfil_alumno.html', context)
    else:
        alumno = Alumno.objects.get(email=request.user.email)
        context = {
            'title': 'Perfil de Alumnos',
            'nombre_alumnos': alumno.nombre,
            'apellido_alumnos': alumno.apellido,
            'matricula_alumnos': alumno.matricula,
            'carrera_alumnos': alumno.carrera,
            'cuatrimestre_alumnos': alumno.cuatrimestre,
            'numero_telefono_alumnos': alumno.numero_telefono,
            'fecha_nacimiento_alumnos': alumno.fecha_nacimiento,
            'direccion_alumnos': alumno.direccion,
            'tipo_alumno_alumnos': alumno.tipo_alumno,
            'email_alumnos': alumno.email,
        }
        return render(request, 'Alumnos/perfil/perfil_alumno.html', context)


@no_cache
@login_required
def Panel_alumnos(request):
    alumno = Alumno.objects.get(email=request.user.email)

    context = {
        'title': 'Panel de Alumnos',
        'nombre_alumnos': alumno.nombre,
        'apellido_alumnos': alumno.apellido,
        'matricula_alumnos': alumno.matricula,
        'carrera_alumnos': alumno.carrera,
        'cuatrimestre_alumnos': alumno.cuatrimestre,
        'numero_telefono_alumnos': alumno.numero_telefono,
        'fecha_nacimiento_alumnos': alumno.fecha_nacimiento,
        'direccion_alumnos': alumno.direccion,
        'tipo_alumno_alumnos': alumno.tipo_alumno,
        'email_alumnos': alumno.email,
    }

    return render(request, 'Alumnos/panel/panel_alumnos.html', context)
