# Generated by Django 4.0.3 on 2022-06-29 22:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('empleador', '0003_alter_infoempleadormodel_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='infoempleadormodel',
            name='user_id',
            field=models.OneToOneField(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Empresa_id'),
        ),
    ]
