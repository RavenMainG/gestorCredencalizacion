from django.shortcuts import render, redirect

def Home(request):

    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('panel_solicitudes_administrador')
        else:
            return redirect('panel_alumnos')

    return render(request, 'Home/Home.html')
