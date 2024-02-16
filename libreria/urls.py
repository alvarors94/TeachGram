from django.urls import path
from . import views # el . indica que de esta misma carpeta, importe views.py

urlpatterns = [
    path("", views.inicio, name="inicio"), # "" indica la ruta 127.0.0.1:8000
    path("publicaciones", views.publicaciones, name="publicaciones"), 
    path("comentarios", views.comentarios, name="comentarios"), 
    path("perfil", views.perfil, name="perfil"), 

]