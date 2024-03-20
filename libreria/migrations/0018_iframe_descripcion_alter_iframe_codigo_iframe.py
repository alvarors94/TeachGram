# Generated by Django 5.0.2 on 2024-03-20 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libreria', '0017_iframe'),
    ]

    operations = [
        migrations.AddField(
            model_name='iframe',
            name='descripcion',
            field=models.CharField(default='¡Echa un vistazo a este recurso!', max_length=200, verbose_name='Descripción'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='iframe',
            name='codigo_iframe',
            field=models.TextField(verbose_name='Iframe'),
        ),
    ]
