# Generated by Django 5.0.2 on 2024-03-11 16:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('libreria', '0014_delete_actividad'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='perfil',
            name='is_active',
        ),
    ]
