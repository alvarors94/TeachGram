from django.urls import path
from . import views # el . indica que de esta misma carpeta, importe views.py
from django.conf import settings # para usar estos archivos en la carpeta settings
from django.contrib.staticfiles.urls import static # para usar estos archivos en la carpeta static

urlpatterns = [
    path("", views.inicio, name="inicio"), # "" indica la ruta 127.0.0.1:8000
    path("perfil", views.perfil, name="perfil"),
    path("crear_publicacion", views.crear_publicacion, name="crear_publicacion"), 
    path("editar_publicacion/<int:id>", views.editar_publicacion, name="editar_publicacion"), 
    path("eliminar_publicacion/<int:id>", views.eliminar_publicacion, name="eliminar_publicacion"), 


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # así concatenamos el path de la carpeta media y la ruta de la carpeta static