# Generated by Django 5.0.2 on 2024-03-06 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libreria', '0012_alter_imagen_imagen'),
    ]

    operations = [
        migrations.CreateModel(
            name='Actividad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100)),
                ('descripcion', models.CharField(max_length=400)),
                ('inicio', models.DateTimeField()),
                ('fin', models.DateTimeField()),
                ('ubicacion', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.AlterModelOptions(
            name='comentario',
            options={'ordering': ['-id']},
        ),
        migrations.AlterModelOptions(
            name='publicacion',
            options={'ordering': ['-id']},
        ),
    ]
