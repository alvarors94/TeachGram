# Generated by Django 5.0.2 on 2024-02-22 17:47

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('libreria', '0004_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(blank=True, max_length=200, null=True, verbose_name='Nombre completo')),
                ('profile_pic', models.ImageField(blank=True, default='media/avatar.png', upload_to='media/profile_pics', verbose_name='Foto de perfil')),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('username', models.OneToOneField(max_length=200, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Nombre de usuario')),
            ],
        ),
        migrations.CreateModel(
            name='Publicacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('foto_publicacion', models.ImageField(upload_to='publicaciones', verbose_name='Imagen')),
                ('descripcion', models.CharField(max_length=200, verbose_name='Descripción')),
                ('fecha_publicacion', models.DateField(auto_now_add=True, verbose_name='Fecha de publicación')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='publicacion', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-fecha_publicacion'],
            },
        ),
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comentario', models.CharField(max_length=400, verbose_name='Comentario')),
                ('fecha_publicacion_comentario', models.DateField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comentario', to=settings.AUTH_USER_MODEL)),
                ('publicacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='libreria.publicacion')),
            ],
        ),
    ]
