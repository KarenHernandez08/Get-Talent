# Generated by Django 4.0.3 on 2022-05-11 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('infopersonal', '0002_infopesonalmodel_age'),
    ]

    operations = [
        migrations.AddField(
            model_name='infopesonalmodel',
            name='video',
            field=models.URLField(default='', unique=True),
            preserve_default=False,
        ),
    ]
