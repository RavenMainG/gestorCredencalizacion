from django.shortcuts import render, redirect
from .models import Alumno
from django.contrib.auth import authenticate, login, logout
# Create your views here.


def login_alumnos(request):
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

def registro_alumnos(request):

    if request.method == 'POST':
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
            )
            context = {
                'mensaje': 'Usuario registrado correctamente'
            }
            return render(request, 'Login/registro_alumnos/registro_alumnos.html', context)

    else:
        return render(request, 'Login/registro_alumnos/registro_alumnos.html')