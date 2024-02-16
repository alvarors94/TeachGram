from django.contrib import admin
from .models import Usuario, Publicacion, Comentario #Importamos las clases

admin.site.register(Usuario)
admin.site.register(Publicacion)
admin.site.register(Comentario)

# Register your models here.
# En la consola tenemos que escribir python manage.py createsuperuser para que nos pida los datos del superusuario