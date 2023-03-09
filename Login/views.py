from django.shortcuts import render

# Create your views here.

def login_administradores(request):
    return render(request, 'login_administradores/login_administradores.html')
def login_alumnos(request):
    return render(request, 'Login/login_alumnos.html')

def login_administradores(request):
    return render(request, 'Login/login_administradores.html')

def registro_alumnos(request):

    if request.method == 'POST':
        datosAlumnos = {
            'nombre': request.POST['nombre'],
            'apellido': request.POST['apellido'],
            'email': request.POST['email'],
            'password': request.POST['password'],
            'password2': request.POST['password2'],
            'carrera': request.POST['carrera'],
            'cuatrimestre': request.POST['cuatrimestre'],
            'matricula': request.POST['matricula'],
            'numero_telefono': request.POST['numero_telefono'],
            'fecha_nacimiento': request.POST['fecha_nacimiento'],
        }

        if datosAlumnos['password'] != datosAlumnos['password2']:
            context = {
                'error': 'Las contraseñas no coinciden'

            }
    else:
        return render(request, 'registro_alumnos/registro_alumnos.html')