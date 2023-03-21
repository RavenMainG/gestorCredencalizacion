from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password, make_password

from django.http.response import HttpResponse

from reportlab.pdfgen import canvas


from Login.models import Alumno, Credencial, Solicitud

import qrcode


def no_cache(view_func):
    def wrapped_view(*args, **kwargs):
        response = view_func(*args, **kwargs)
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        return response

    return wrapped_view




@no_cache
@login_required
def Solicitudes_Alumnos(request):

    if request.user.is_superuser:
        return redirect('panel_solicitudes_administrador')

    alumno = Alumno.objects.get(email=request.user.email)

    if request.method == 'POST':
        alumno.crear_solicitud()
        context = {
            'title': 'Solicitud de alumnos',
            'mensaje': 'Tu solicitud ya fue enviada, espera a que un administrador la revise',
            'permite_solicitud': False,
            'solicitud': alumno.obtener_solicitud()
        }
        return render(request, 'Alumnos/solicitudes/solicitudes_alunno.html', context)

    else:
        if alumno.ficha_medica_existe() == False or alumno.contacto_emergencia_existe() == False:
            context = {
                'title': 'Solicitud de alumnos',
                'mensaje': 'No puedes enviar una solicitud, primero debes llenar tus de emergencia y ficha medica',
                'permite_solicitud': False,
                'solicitud': alumno.obtener_solicitud()
            }
            return render(request, 'Alumnos/solicitudes/solicitudes_alunno.html', context)
        else:
            if alumno.estado_credencial() == 'Inactiva':
                if alumno.estado_solicitud() == 'Rechazada':
                    context = {
                        'title': 'Solicitud de alumnos',
                        'mensaje': 'Tu credencial esta inactiva y tu solicitud fue rechazada, puedes volver a enviar una solicitud',
                        'permite_solicitud': True,
                        'solicitud': alumno.obtener_solicitud()
                    }
                    return render(request, 'Alumnos/solicitudes/solicitudes_alunno.html', context)
                elif alumno.estado_solicitud() == 'Pendiente':
                    context = {
                        'title': 'Solicitud de alumnos',
                        'mensaje': 'Tu credencial esta inactiva y tu solicitud esta pendiente, espera a que un administrador la revise',
                        'permite_solicitud': False,
                        'solicitud': alumno.obtener_solicitud()
                    }
                    return render(request, 'Alumnos/solicitudes/solicitudes_alunno.html', context)
                else:
                    context = {
                        'title': 'Solicitud de alumnos',
                        'mensaje': 'Tu credencial esta inactiva y puedes enviar una solicitud',
                        'permite_solicitud': True,
                        'solicitud': alumno.obtener_solicitud()
                    }
                    return render(request, 'Alumnos/solicitudes/solicitudes_alunno.html', context)

            else:
                context = {
                    'title': 'Solicitud de alumnos',
                    'mensaje': 'Tu credencial esta activa',
                    'permite_solicitud': False,
                    'solicitud': alumno.obtener_solicitud()
                }
                return render(request, 'Alumnos/solicitudes/solicitudes_alunno.html', context)


@no_cache
@login_required
def Cambiar_password(request):

    if request.user.is_superuser:
        return redirect('panel_solicitudes_administrador')

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

    if request.user.is_superuser:
        return redirect('panel_solicitudes_administrador')

    if request.method == 'POST':
        alumno = Alumno.objects.get(email=request.user.email)

        alumno.nombre = request.POST['nombres']
        alumno.apellido = request.POST['apellidos']
        alumno.matricula = request.POST['matricula']
        alumno.numero_telefono = request.POST['numero_telefono']
        alumno.fecha_nacimiento = request.POST['fecha_nacimiento']
        alumno.direccion = request.POST['direccion']
        # alumno.email = request.POST['email']
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
            'mensaje': 'Se actualizo tu perfil'
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

    if request.user.is_superuser:
        return redirect('panel_solicitudes_administrador')
    alumno = Alumno.objects.get(email=request.user.email)
    if request.POST == 'POST':
        url = alumno.imagen.url
        nueva_url = url.split('/')
        url = nueva_url[nueva_url.__len__() - 2] + "/" + nueva_url[nueva_url.__len__() - 1]

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
            'estado_credencial': alumno.credencial.estado_credencial,
            'imagen': url,
        }

        print(url)

        return render(request, 'Alumnos/panel/panel_alumnos.html', context)
    else:

        url = alumno.imagen.url
        nueva_url = url.split('/')
        url = nueva_url[nueva_url.__len__() - 2] + "/" + nueva_url[nueva_url.__len__() - 1]

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
            'estado_credencial': alumno.credencial.estado_credencial,
            'imagen': url,
        }

        print(url)

        return render(request, 'Alumnos/panel/panel_alumnos.html', context)


@no_cache
@login_required
def Ficha_medica(request):

    if request.user.is_superuser:
        return redirect('panel_solicitudes_administrador')

    alumno = Alumno.objects.get(email=request.user.email)
    if request.method == 'POST':

        alumno.crear_ficha_medica(request.POST['tipo_sangre'], request.POST['alergias'], request.POST['enfermedades'],
                                  request.POST['medicamentos'])
        alumno.crear_contacto_emergencia(request.POST['nombre_contacto'], request.POST['telefono_emergencia'],
                                         request.POST['parentesco_emergencia'])

        context = {
            'title': 'Ficha medica',
            'mensaje': 'Se ha guardado tu ficha medica'
        }
        return render(request, 'Alumnos/ficha_medica/ficha_medica.html', context)

    else:

        if alumno.ficha_medica_existe() and alumno.contacto_emergencia_existe():

            context = {
                'title': 'Ficha medica',
                'tipo_sangre': alumno.ficha_medica.tipo_sangre,
                'alergias': alumno.ficha_medica.alergias,
                'enfermedades': alumno.ficha_medica.enfermedades,
                'medicamentos': alumno.ficha_medica.medicamentos,
                'nombre_contacto': alumno.contacto_emergencia.nombre,
                'telefono_emergencia': alumno.contacto_emergencia.numero_telefono,
                'parentesco_emergencia': alumno.contacto_emergencia.parentesco,

            }
        else:
            context = {
                'title': 'Ficha medica',
            }

        return render(request, 'Alumnos/ficha_medica/ficha_medica.html', context)


def Ruta_qr_alumno(request, matricula):
    alumno = Alumno.objects.get(matricula=matricula)

    print(alumno.nombre)
    contex = {
        'nombre': alumno.nombre,
        'apellidos': alumno.apellido,
        'matricula': alumno.matricula,
        'correo': alumno.email,
        # Datos de emergencia y contacto

        'Alergias': alumno.ficha_medica.alergias,
        'tipo_sangre': alumno.ficha_medica.tipo_sangre,
        'enfermedades': alumno.ficha_medica.enfermedades,
        'medicamentos': alumno.ficha_medica.medicamentos,

        'nombre_contacto_emergencia': alumno.contacto_emergencia.nombre,
        'numero_contacto_emergencia': alumno.contacto_emergencia.numero_telefono,

    }

    return render(request, 'Alumnos/pagina_qr_alumno/pagina_qr_alumno.html', contex)

def Generar_credencial_pdf(request, matricula):
    # Obtener los datos del modelo
    datos = Alumno.objects.get(matricula=matricula)


    # Crear un objeto para el PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="archivo.pdf"'
    p = canvas.Canvas(response)

    # Escribir los datos en el PDF
    for dato in datos:
        p.drawString(100, 100, str(dato))

    # Cerrar el objeto del PDF y devolverlo
    p.showPage()
    p.save()
    return response

def Credencial_pdf(request):
    alumno = Alumno.objects.get(email=request.user.email)
    url = alumno.imagen.url
    nueva_url = url.split('/')
    url = nueva_url[nueva_url.__len__() - 2] + "/" + nueva_url[nueva_url.__len__() - 1]
    if(alumno.credencial.estado_credencial == 'Activa'):
        permite_descargar = True
    else:
        permite_descargar = False
    context = {
        'alumno': alumno,
        'imagen': url,
        'permite_descargar': permite_descargar,
    }
    return render(request, 'Alumnos/credencial/credencial.html', context)


