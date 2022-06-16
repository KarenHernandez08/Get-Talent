# Generated by Django 4.0.3 on 2022-06-16 19:34

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='InfoAcademicaModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('institucion', models.CharField(max_length=100)),
                ('fecha_inicio', models.DateField(default='0000-00-00', null=True)),
                ('fecha_fin', models.DateField(default='0000-00-00', null=True)),
                ('nivel_escolar', models.CharField(choices=[('Carrera Técnica', 'Carrera Tecnica'), ('Universidad', 'Universidad'), ('Maestría', 'Maestria'), ('Doctorado', 'Doctorado'), ('Diplomado', 'Diplomado'), ('Curso', 'Curso'), ('Certificación', 'Certificación'), ('Otro', 'Otro'), ('sin especificar', 'Sinespecificar')], default='sin especificar', max_length=20)),
                ('estatus_academico', models.CharField(choices=[('Finalizado', 'Finalizado'), ('En curso', 'En Curso'), ('Trunco', 'Trunco'), ('Otro', 'Otro'), ('sin especificar', 'Sinespecificar')], default='sin especificar', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='InfoPesonalModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('middle_name', models.CharField(max_length=30)),
                ('paternal_lastname', models.CharField(max_length=30)),
                ('maternal_lastname', models.CharField(max_length=30)),
                ('date_birth', models.DateField(blank=True)),
                ('age', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(16), django.core.validators.MaxValueValidator(100)])),
                ('additional_mail', models.EmailField(blank=True, default='null', max_length=50)),
                ('gender', models.CharField(choices=[('femenino', 'Femenino'), ('masculino', 'Masculino'), ('otro', 'Otro'), ('sin especificar', 'Sinespecificar')], default='sin especificar', max_length=20)),
                ('marital_status', models.CharField(choices=[('soltero', 'Soltero'), ('casado', 'Casado'), ('otro', 'Otro'), ('sin especificar', 'Sinespecificar')], default='sin especificar', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='VideoSolicitanteModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video', models.URLField(max_length=2000, unique=True)),
            ],
        ),
    ]
