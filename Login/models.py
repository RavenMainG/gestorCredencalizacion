from django.core.exceptions import ValidationError
from django.db import models
from datetime import datetime

# importaciones para la moddificacion del modelo de usuario
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


# Inicio de mod
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El usuario debe de tener un correo')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, error_messages={'unique': 'Ya existe un usuario con este correo'})
    nombre = models.CharField(max_length=50, blank=True)
    apellido = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    is_alumno = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_join = models.DateTimeField(auto_now_add=True)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def clean(self):
        super().clean()
        if self.email and not self.email.endswith('@uptapachula.edu.mx'):
            raise ValidationError('Solo se permiten correos electrónicos con el dominio @uptapachula.edu.mx')

    def get_full_name(self):
        nombre_completo = f'{self.nombre} {self.apellido}'
        return nombre_completo.strip()

    def get_short_name(self):
        return self.nombre





class Alumno(User):
    matricula = models.CharField(max_length=10, unique=True,
                                 error_messages={'unique': 'Ya existe un usuario con esta matricula'})
    carrera = models.CharField(max_length=50)
    cuatrimestre = models.CharField(max_length=3)
    numero_telefono = models.CharField(max_length=10)
    fecha_nacimiento = models.DateField()

    def __str__(self) -> str:
        return self.nombre


class Credencial(models.Model):
    alumno = models.OneToOneField(Alumno, on_delete=models.CASCADE)
    estado_credencial = models.CharField(max_length=10)

    def __str__(self) -> str:
        return self.estado_credencial

class Solicitud(models.Model):
    tipo_solicitud = models.CharField(max_length=50)
    estado_solicitud = models.CharField(max_length=50)
    fecha_solicitud = models.DateField(default=datetime.now)
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.tipo_solicitud


class Administrador(User):
    def __str__(self) -> str:
        return self.nombre