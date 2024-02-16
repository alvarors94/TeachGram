from django.shortcuts import render
from .models import Usuario, Publicacion, Comentario #Importamos las clases

def inicio(request):
    return render(request, "paginas/inicio.html")

def perfil(request):
    usuarios = Usuario.objects.all()
    return render(request, "perfil/index.html", {"usuarios": usuarios})

def crear_publicacion(request):
    return render(request, "perfil/crear_publicacion.html")

def editar_publicacion(request):
    return render(request, "perfil/editar_publicacion.html")

def eliminar_publicacion(request):
    return render(request, "perfil/eliminar_publicacion.html")