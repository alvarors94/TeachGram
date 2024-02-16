from django.shortcuts import render
from django.http import HttpResponse

def inicio(request):
    return render(request, "paginas/inicio.html")

def perfil(request):
    return render(request, "paginas/perfil.html")

def publicaciones(request):
    return render(request, "publicaciones/index.html")

def comentarios(request):
    return render(request, "comentarios/index.html")
