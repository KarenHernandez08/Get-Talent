# Generated by Django 4.0.3 on 2022-07-18 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vacantes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vacantesmodel',
            name='experiencia',
            field=models.CharField(choices=[('Becario', 'Becario'), ('Primer Empleo', 'Primer Empleo'), ('Poca Experiencia', 'Poca Experiencia'), ('Experiencia Media', 'Experiencia Media'), ('Mucha experiencia', 'Mucha Experiencia'), ('Cargos ejecutivos', 'Cargos ejecutivos')], max_length=60),
        ),
    ]