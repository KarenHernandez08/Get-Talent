# Generated by Django 4.0.3 on 2022-07-04 22:29

from django.db import migrations



    dependencies = [
        ('empleador', '0007_alter_infoempleadormodel_user_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='infoempleadormodel',
            old_name='name',
            new_name='empresa',
        ),
    ]
