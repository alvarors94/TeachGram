from django.shortcuts import render
from django.http import HttpResponse

def inicio(request):
    return render(request, "paginas/inicio.html")

def perfil(request):
    return render(request, "perfil/index.html")

def crear_publicacion(request):
    return render(request, "perfil/crear_publicacion.html")

def editar_publicacion(request):
    return render(request, "perfil/editar_publicacion.html")

def eliminar_publicacion(request):
    return render(request, "perfil/eliminar_publicacion.html")