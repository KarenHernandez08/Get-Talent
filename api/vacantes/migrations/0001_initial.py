# Generated by Django 4.0.3 on 2022-04-24 01:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AreasModel',
            fields=[
                ('areas_id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('status', models.BooleanField(default=False)),
                ('nombre_area', models.CharField(max_length=150)),
            ],
            options={
                'db_table': 'Áreas de Interes',
            },
        ),
        migrations.CreateModel(
            name='InteresesAreasModel',
            fields=[
                ('interesesareas_id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('areas_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='vacantes.areasmodel')),
            ],
            options={
                'db_table': 'Intereses por Área',
            },
        ),
        migrations.CreateModel(
            name='RolesModel',
            fields=[
                ('rol_id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('rol', models.CharField(max_length=150)),
            ],
            options={
                'db_table': 'Roles',
            },
        ),
        migrations.CreateModel(
            name='VacantesModel',
            fields=[
                ('vacante_id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('is_active', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('descripcion', models.TextField(max_length=500)),
                ('requisitos', models.TextField(max_length=300)),
                ('vacante_video', models.CharField(max_length=150)),
                ('sueldo', models.DecimalField(decimal_places=2, max_digits=30)),
                ('tipo_trabajo', models.CharField(choices=[('Tiempo Completo', 'Tiempo Completo'), ('Medio Tiempo', 'Medio Tiempo'), ('Proyecto', 'Proyecto')], max_length=20)),
                ('modalidad', models.CharField(choices=[('Presencial', 'Presencial'), ('Virtual', 'Virtual'), ('Hibrido', 'Hibrido')], max_length=20)),
                ('localidad', models.CharField(choices=[('Aguascalientes', 'Aguascalientes'), ('Baja California', 'Baja California'), ('Baja California Sur', 'Baja California Sur'), ('Campeche', 'Campeche'), ('Chiapas', 'Chiapas'), ('Chihuahua', 'Chihuahua'), ('Ciudad de México', 'Cd Mex'), ('Coahuila', 'Coahuila'), ('Colima', 'Colima'), ('Durango', 'Durango'), ('Guanajuato', 'Guanajuato'), ('Guerrero', 'Guerrero'), ('Hidalgo', 'Hidalgo'), ('Jalisco', 'Jalisco'), ('Estado de México', 'Edo Mex'), ('Michoacán', 'Michoacan'), ('Morelos', 'Morelos'), ('Nayarit', 'Nayarit'), ('Nuevo León', 'Nuevo Leon'), ('Oaxaca', 'Oaxaca'), ('Puebla', 'Puebla'), ('Querétaro', 'Queretaro'), ('Quintana Roo', 'Quintana Roo'), ('San Luis Potosí', 'San Luis Potosi'), ('Sinaloa', 'Sinaloa'), ('Sonora', 'Sonora'), ('Tabasco', 'Tabasco'), ('Tamaulipas', 'Tamaulipas'), ('Tlaxcala', 'Tlaxcala'), ('Veracruz', 'Veracruz'), ('Yucatán', 'Yucatan'), ('Zacatecas', 'Zacatecas')], max_length=25)),
                ('area_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='vacantes.areasmodel')),
                ('roles_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='vacantes.rolesmodel')),
            ],
        ),
        migrations.CreateModel(
            name='VacantesAreasModel',
            fields=[
                ('vacantesareas_id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('areas_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='vacantes.areasmodel')),
                ('vacante_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='vacantes.vacantesmodel')),
            ],
            options={
                'db_table': 'Vacantes por Área',
            },
        ),
        migrations.CreateModel(
            name='RolVacantesModel',
            fields=[
                ('rolvacante', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('rol_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='vacantes.rolesmodel')),
                ('vacantesareas_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='vacantes.vacantesareasmodel')),
            ],
            options={
                'db_table': 'Roles para Vacantes',
            },
        ),
        migrations.CreateModel(
            name='RolAreasModel',
            fields=[
                ('rolareas_id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('interesesareas_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='vacantes.interesesareasmodel')),
                ('rol_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='vacantes.rolesmodel')),
            ],
            options={
                'db_table': 'Roles por Área',
            },
        ),
        migrations.CreateModel(
            name='PreguntasModel',
            fields=[
                ('preguntas_id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('pregunta1', models.CharField(max_length=150)),
                ('pregunta2', models.CharField(max_length=150)),
                ('pregunta3', models.CharField(max_length=150)),
                ('status', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha creación')),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('vacante_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='vacantes.vacantesmodel')),
            ],
            options={
                'db_table': 'Preguntas para Vacantes',
            },
        ),
    ]