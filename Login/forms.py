from django.forms import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Alumno, Credencial
from .models import Administrador

class RegistrarAdministrador( UserCreationForm):
    class Meta:
        model = Administrador
        fields = ['email', 'password1', 'password2']


