# Generated by Django 4.1.7 on 2023-03-18 14:33

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contacto_emergencia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_telefono', models.CharField(max_length=10)),
                ('nombre', models.CharField(max_length=50)),
                ('parentesco', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Credencial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado_credencial', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Ficha_medica',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_sangre', models.CharField(max_length=3)),
                ('alergias', models.CharField(max_length=50)),
                ('enfermedades', models.CharField(max_length=50)),
                ('medicamentos', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Solicitud',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_solicitud', models.CharField(max_length=50)),
                ('estado_solicitud', models.CharField(max_length=50)),
                ('fecha_solicitud', models.DateField(default=datetime.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(error_messages={'unique': 'Ya existe un usuario con este correo'}, max_length=254, unique=True)),
                ('nombre', models.CharField(blank=True, max_length=50)),
                ('apellido', models.CharField(blank=True, max_length=50)),
                ('is_active', models.BooleanField(default=True)),
                ('is_alumno', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('date_join', models.DateTimeField(auto_now_add=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Administrador',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=('Login.user',),
        ),
        migrations.CreateModel(
            name='Alumno',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('matricula', models.CharField(error_messages={'unique': 'Ya existe un usuario con esta matricula'}, max_length=10, unique=True)),
                ('carrera', models.CharField(max_length=50)),
                ('cuatrimestre', models.CharField(max_length=3)),
                ('numero_telefono', models.CharField(max_length=10)),
                ('fecha_nacimiento', models.DateField()),
                ('direccion', models.CharField(max_length=100)),
                ('tipo_alumno', models.CharField(max_length=50)),
                ('imagen', models.ImageField(upload_to='Login/static/imagenes/')),
                ('contacto_emergencia', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Login.contacto_emergencia')),
                ('credencial', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Login.credencial')),
                ('ficha_medica', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Login.ficha_medica')),
                ('solicitud', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='solicitud', to='Login.solicitud')),
            ],
            options={
                'abstract': False,
            },
            bases=('Login.user',),
        ),
        migrations.CreateModel(
            name='Historial_solicitud',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_solicitud', models.CharField(max_length=50)),
                ('estado_solicitud', models.CharField(max_length=50)),
                ('fecha_solicitud', models.DateField(default=datetime.datetime.now)),
                ('alumno', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='alumno', to='Login.alumno')),
            ],
        ),
    ]
