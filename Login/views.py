from django.shortcuts import render, redirect
from .models import Alumno, Credencial
from django.contrib.auth import authenticate, login, logout

from pathlib import Path

from .forms import RegistrarAdministrador

from PIL import Image

import os

import qrcode
from django.http.response import HttpResponse


def login_alumnos(request):

    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('panel_solicitudes_administrador')
        else:
            return redirect('panel_alumnos')

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            context = {
                'mensaje': 'Usuario logeado correctamente'
            }

            return redirect('panel_alumnos')
        else:
            context = {
                'error': 'Usuario o contraseña incorrectos'
            }
            return render(request, 'Login/login_alumno/login_alumno.html', context)
    else:
        return render(request, 'Login/login_alumno/login_alumno.html')

def logout_alumnos(request):
    logout(request)
    return redirect('home')


def modificacion_fecha(fecha):
    fecha_separada = fecha

def registro_alumnos(request):

    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('panel_solicitudes_administrador')
        else:
            return redirect('panel_alumnos')

    if request.method == 'POST':
        print(request.POST['fecha_nacimiento'])
        fecha = request.POST['fecha_nacimiento']

        datosAlumnos = {
            'nombres': request.POST['nombres'],
            'apellidos': request.POST['apellidos'],
            'email': request.POST['email'],
            'password1': request.POST['password1'],
            'password2': request.POST['password2'],
            'carrera': request.POST['carrera'],
            'cuatrimestre': request.POST['cuatrimestre'],
            'matricula': request.POST['matricula'],
            'numero_telefono': request.POST['numero_telefono'],
            'fecha_nacimiento': request.POST['fecha_nacimiento'],
            'direccion': request.POST['direccion'],
            'tipo_alumno': request.POST['tipo_alumno'],
            'imagen': request.FILES.get('imagen')
        }


        print(datosAlumnos)

        if datosAlumnos['password1'] != datosAlumnos['password2']:
            context = {
                'error': 'Las contraseñas no coinciden'

            }
            return render(request, 'Login/registro_alumnos/registro_alumnos.html', context)
        else:

            nuevo_alumno = Alumno.objects.create_user(
                email=datosAlumnos['email'],
                password=datosAlumnos['password1'],
                nombre=datosAlumnos['nombres'],
                apellido=datosAlumnos['apellidos'],
                matricula=datosAlumnos['matricula'],
                carrera=datosAlumnos['carrera'],
                cuatrimestre=datosAlumnos['cuatrimestre'],
                numero_telefono=datosAlumnos['numero_telefono'],
                fecha_nacimiento=datosAlumnos['fecha_nacimiento'],
                direccion=datosAlumnos['direccion'],
                tipo_alumno=datosAlumnos['tipo_alumno'],
                imagen=datosAlumnos['imagen'],
            )

            alumnos = Alumno.objects.get(email=datosAlumnos['email'])
            alumnos.crear_credencial_alumno()

            context = {
                'mensaje': 'Usuario registrado correctamente'
            }
            return render(request, 'Login/registro_alumnos/registro_alumnos.html', context)

    else:
        return render(request, 'Login/registro_alumnos/registro_alumnos.html')

def registra_admin(request):
    formAdmin = RegistrarAdministrador()

    if request.method == 'POST':
        formAdmin = RegistrarAdministrador(request.POST)
        if formAdmin.is_valid():
            formAdmin.save()
            return redirect('home')
        else:
            context = {
                'error': 'Error al registrar'
            }
            return render(request, 'Login/registro_admin/registro_admin.html', context)
    else:
        context = {
            'formAdmin': formAdmin
        }
        return render(request, 'Login/registro_admin/registro_admin.html', context)
        

def Login_admin(request):

    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('panel_solicitudes_administrador')
        else:
            return redirect('panel_alumnos')

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            context = {
                'mensaje': 'Usuario logeado correctamente'
            }

            return redirect('panel_solicitudes_administrador')
        else:
            context = {
                'error': 'Usuario o contraseña incorrectos'
            }
            return render(request, 'Login/login_administrador/login_administrador.html', context)
    else:
        return render(request, 'Login/login_administrador/login_administrador.html')

def Qr(request, matricula):

    alumno = Alumno.objects.get(matricula=matricula)

    url = f'http://127.0.0.1:8000/panel_alumnos/ruta_qr_alumno/{alumno.matricula}'

    # ruta_imagen = os.path.join()
    BASE_DIR = Path(__file__).resolve().parent.parent

    print(f"ruta: {BASE_DIR}")

    logo_ruta = os.path.join(BASE_DIR, 'static/imagenes/LogoUPTap.png')

    logo = Image.open(logo_ruta)

    basewidth = 100

    wpercent = (basewidth / float(logo.size[0]))
    hsize = int((float(logo.size[1]) * float(wpercent)))
    logo = logo.resize((basewidth, hsize), Image.ANTIALIAS)
    QRcode = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H
    )
    QRcode.add_data(url)

    QRcode.make()
    QRcolor = 'Black'

    QRimg = QRcode.make_image(
        fill_color=QRcolor, back_color="white").convert('RGB')

    pos = ((QRimg.size[0] - logo.size[0]) // 2,
           (QRimg.size[1] - logo.size[1]) // 2)
    QRimg.paste(logo, pos)

    response = HttpResponse(content_type="image/png")
    QRimg.save(response, "PNG")
    return response

