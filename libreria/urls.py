from django.urls import path
from . import views # el . indica que de esta misma carpeta, importe views.py

urlpatterns = [
    path("", views.inicio, name="inicio"), # "" indica la ruta 127.0.0.1:8000
    path("perfil", views.perfil, name="perfil"),
    path("crear_publicacion", views.crear_publicacion, name="publicar"), 
    path("editar_publicacion", views.editar_publicacion, name="editar_publicacion"), 
    path("eliminar_publicacion", views.eliminar_publicacion, name="eliminar_publicacion"), 
 

]