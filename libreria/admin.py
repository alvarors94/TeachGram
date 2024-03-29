from django.contrib import admin
from .models import Perfil, Publicacion, Comentario, Imagen, Recursos, Iframe #Importamos las clases

admin.site.register(Perfil)
admin.site.register(Publicacion)
admin.site.register(Comentario)
admin.site.register(Imagen)
admin.site.register(Recursos)
admin.site.register(Iframe)

# Register your models here.
# En la consola tenemos que escribir python manage.py createsuperuser para que nos pida los datos del superusuario