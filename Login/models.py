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
    imagen = models.ImageField(upload_to='Login/static/imagenes/')

    ficha_medica = models.OneToOneField('Ficha_medica', on_delete=models.CASCADE, null=True, blank=True)
    contacto_emergencia = models.OneToOneField('Contacto_emergencia', on_delete=models.CASCADE, null=True, blank=True)

    credencial = models.OneToOneField('Credencial', on_delete=models.CASCADE, null=True, blank=True)

    solicitud = models.OneToOneField('Solicitud', on_delete=models.CASCADE, null=True, blank=True, related_name='solicitud')


    # ACTUALIZACIONES DE DATOS
    def actualizar_datos_ficha_medica(self, tipo_sangre, alergias, enfermedades, medicamentos):
        if tipo_sangre:
            self.ficha_medica.tipo_sangre = tipo_sangre
        elif alergias:
            self.ficha_medica.alergias = alergias
        elif enfermedades:
            self.ficha_medica.enfermedades = enfermedades
        elif medicamentos:
            self.ficha_medica.medicamentos = medicamentos
        self.ficha_medica.save()

    def actualizar_datos_contacto_emergencia(self, nombre, apellido, numero_telefono, parentesco):
        if nombre:
            self.contacto_emergencia.nombre = nombre
        elif apellido:
            self.contacto_emergencia.apellido = apellido
        elif numero_telefono:
            self.contacto_emergencia.numero_telefono = numero_telefono
        elif parentesco:
            self.contacto_emergencia.parentesco = parentesco
        self.contacto_emergencia.save()



    def crear_contacto_emergencia(self, nombre, numero_telefono, parentesco):
        if self.contacto_emergencia:
            self.contacto_emergencia.nombre = nombre
            self.contacto_emergencia.numero_telefono = numero_telefono
            self.contacto_emergencia.parentesco = parentesco
            self.contacto_emergencia.save()

        else:
            contacto_emergencia = Contacto_emergencia.objects.create(
                nombre=nombre,
                numero_telefono=numero_telefono,
                parentesco=parentesco,
            )
            self.contacto_emergencia = contacto_emergencia
            self.save()

    def ficha_medica_existe(self):
        if self.ficha_medica:
            return True
        else:
            return False

    def contacto_emergencia_existe(self):
        if self.contacto_emergencia:
            return True
        else:
            return False
    def crear_ficha_medica(self, tipo_sangre, alergias, enfermedades, medicamentos):
        if self.ficha_medica_existe():

            self.ficha_medica.tipo_sangre = tipo_sangre
            self.ficha_medica.alergias = alergias
            self.ficha_medica.enfermedades = enfermedades
            self.ficha_medica.medicamentos = medicamentos
            self.ficha_medica.save()

        else:
            ficha_medica = Ficha_medica.objects.create(
                tipo_sangre=tipo_sangre,
                alergias=alergias,
                enfermedades=enfermedades,
                medicamentos=medicamentos,
            )
            self.ficha_medica = ficha_medica
            self.save()

    def estado_credencial(self):
        if self.credencial:
            return self.credencial.estado_credencial
        else:
            return None

    def obtener_solicitud(self):
        if self.solicitud:
            return self.solicitud
        else:
            return None


    def solicitud_existe(self):
        if self.solicitud:
            return True
        else:
            return False

    def crear_solicitud(self):
        if self.solicitud_existe():
            print('Ya existe una solicitud')
            self.solicitud.estado_solicitud = 'Pendiente'
            self.solicitud.fecha_solicitud = datetime.now()
            self.solicitud.tipo_solicitud = 'Reposicion'
            self.solicitud.save()
        else:
            solicitud = Solicitud.objects.create(
                tipo_solicitud='Primera',
                estado_solicitud='Pendiente',
                fecha_solicitud=datetime.now(),
            )
            self.solicitud = solicitud
            self.save()

    def detalle_solicitud(self):
        if self.solicitud:
            return self.solicitud.estado_solicitud
        else:
            return None


    def estado_solicitud(self):
        if self.solicitud:
            return self.solicitud.estado_solicitud
        else:
            return None

    def aceptar_solicitud(self):
        self.solicitud.estado_solicitud = 'Aceptada'
        self.solicitud.save()
        solicitud_historial = Historial_solicitud.objects.create(
            tipo_solicitud=self.solicitud.tipo_solicitud,
            estado_solicitud=self.solicitud.estado_solicitud,
            fecha_solicitud=self.solicitud.fecha_solicitud,
            alumno=self
        )


    def rechazar_solicitud(self):
        self.solicitud.estado_solicitud = 'Rechazada'
        self.solicitud.save()
        solicitud_historial = Historial_solicitud.objects.create(
            tipo_solicitud=self.solicitud.tipo_solicitud,
            estado_solicitud=self.solicitud.estado_solicitud,
            fecha_solicitud=self.solicitud.fecha_solicitud,
            alumno=self
        )


    def historial_solicitudes_existe(self):
        if historial_solicitud := Historial_solicitud.objects.filter(alumno=self):
            return True
        else:
            return False

    def obtener_historial_solicitudes(self):
        if historial_solicitud := Historial_solicitud.objects.filter(alumno=self):
            return historial_solicitud.filter(alumno=self)
        else:
            return None

    def obtener_credencial_alumno(self):
        return self.credencial

    def crear_credencial_alumno(self):
        self.credencial = Credencial.objects.create(estado_credencial='Inactiva')
        self.save()

    def activar_credencial_alumno(self):
        self.credencial.estado_credencial = 'Activa'
        self.credencial.save()

    def desactivar_credencial_alumno(self):
        self.credencial.estado_credencial = 'Inactiva'
        self.credencial.save()

    def __str__(self) -> str:
        return self.nombre

class Historial_solicitud(models.Model):
    tipo_solicitud = models.CharField(max_length=50)
    estado_solicitud = models.CharField(max_length=50)
    fecha_solicitud = models.DateField(default=datetime.now)
    alumno = models.ForeignKey('Alumno', on_delete=models.CASCADE, null=True, blank=True, related_name='alumno')

    def __str__(self) -> str:
        return self.tipo_solicitud

class Ficha_medica(models.Model):
    tipo_sangre = models.CharField(max_length=3)
    alergias = models.CharField(max_length=50)
    enfermedades = models.CharField(max_length=50)
    medicamentos = models.CharField(max_length=50)

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

class Contacto_emergencia(models.Model):
    numero_telefono = models.CharField(max_length=10)
    nombre = models.CharField(max_length=50)
    parentesco = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.numero_telefono


class Administrador(User):

    def __str__(self) -> str:
        return self.nombre
