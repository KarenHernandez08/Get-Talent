# Generated by Django 4.0.3 on 2022-05-19 04:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solicitantes', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='VideoSolicitanteModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video', models.URLField(unique=True)),
            ],
        ),
    ]