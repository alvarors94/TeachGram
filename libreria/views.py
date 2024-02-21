from django.shortcuts import render, redirect
from .models import  Publicacion, Comentario #Importamos las clases
from .forms import PublicacionForm, ComentarioForm
from django.contrib.auth import logout
from django.contrib.auth.models import User
def inicio(request):
    return render(request, "paginas/inicio.html")

def perfil(request):
    users = User.objects.all()
    return render(request, "perfil/index.html", {"users": users})

from django.shortcuts import redirect

def crear_publicacion(request):
    if request.method == 'POST':
        form_publicacion = PublicacionForm(request.POST, request.FILES)
        if form_publicacion.is_valid():
            publicacion = form_publicacion.save(commit=False)
            publicacion.user_id = request.user.id  # Asigna el id del usuario autenticado
            publicacion.save()
            return redirect("publicaciones")
    else:
        form_publicacion = PublicacionForm()
    
    return render(request, "perfil/crear_publicacion.html", {"form_publicacion": form_publicacion})

def editar_publicacion(request,id):
    publicacion = Publicacion.objects.get(id_publicacion = id)
    form_publicacion = PublicacionForm(request.POST or None, request.FILES or None, instance = publicacion)
    if form_publicacion.is_valid() and request.POST:
        form_publicacion.save()
        return redirect("publicaciones")
    return render(request, "perfil/editar_publicacion.html", {"form_publicacion": form_publicacion})

def eliminar_publicacion(request,id):
    publicacion = Publicacion.objects.get(id_publicacion = id)
    publicacion.delete()
    return redirect("publicaciones")

def ver_publicaciones(request):
    publicaciones = Publicacion.objects.all()
    users = User.objects.all()
    return render(request, "perfil/publicaciones.html", {"publicaciones": publicaciones, "users": users})


def ver_comentarios(request, id):
    publicacion = Publicacion.objects.get(id_publicacion=id)
    comentarios = publicacion.comentarios.all()  # Obtener todos los comentarios de la publicación específica
    return render(request, "perfil/ver_comentarios.html", {"publicacion": publicacion, "comentarios": comentarios})

def agregar_comentario(request, id):
    publicacion = Publicacion.objects.get(id_publicacion=id)
    if request.method == 'POST':
        form_comentario = ComentarioForm(request.POST)
        if form_comentario.is_valid():
            comentario = form_comentario.save(commit=False)
            comentario.publicacion_id = publicacion.id_publicacion
            comentario.user_id = request.user.id  # Asignar el ID del usuario autenticado al campo usuario_id del comentario
            comentario.save()
            return redirect("publicaciones")
    else:
        form_comentario = ComentarioForm(initial={'publicacion': publicacion.id_publicacion})
    return render(request, "perfil/agregar_comentario.html", {"form_comentario": form_comentario, "publicacion": publicacion})
