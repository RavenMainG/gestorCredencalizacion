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
    direccion = models.CharField(max_length=100)
    tipo_alumno = models.CharField(max_length=50)

    ficha_medica = models.OneToOneField('Ficha_medica', on_delete=models.CASCADE, null=True, blank=True)
    credencial = models.OneToOneField('Credencial', on_delete=models.CASCADE, null=True, blank=True)

    solicitud = models.ManyToManyField('Solicitud', blank=True)

    imagen = models.ImageField(upload_to='Login/static/imagenes/')


    def ultima_solicitud_pendiente(self):
        ultima_solicitud = self.solicitud.order_by('-fecha_solicitud').first()
        if ultima_solicitud and ultima_solicitud.estado_solicitud == 'pendiente':
            return True
        return False

    def obtener_ultima_solicitud(self):
        ultima_solicitud = self.solicitud.order_by('-fecha_solicitud').first()
        return ultima_solicitud

    def __str__(self) -> str:
        return self.nombre


class Ficha_medica(models.Model):
    tipo_sangre = models.CharField(max_length=3)
    alergias = models.CharField(max_length=50)
    enfermedades = models.CharField(max_length=50)
    medicamentos = models.CharField(max_length=50)
    fecha_ultima_visita = models.DateField(default=datetime.now)

    def __str__(self) -> str:
        return self.tipo_sangre


class Credencial(models.Model):
    estado_credencial = models.CharField(max_length=10)

    def __str__(self) -> str:
        return self.estado_credencial


class Solicitud(models.Model):
    tipo_solicitud = models.CharField(max_length=50)
    estado_solicitud = models.CharField(max_length=50)
    fecha_solicitud = models.DateField(default=datetime.now)

    def __str__(self) -> str:
        return self.tipo_solicitud


class Administrador(User):
    def __str__(self) -> str:
        return self.nombre
