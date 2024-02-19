from django.shortcuts import render, redirect
from .models import Usuario, Publicacion, Comentario #Importamos las clases
from .forms import PublicacionForm
def inicio(request):
    return render(request, "paginas/inicio.html")

def perfil(request):
    usuarios = Usuario.objects.all()
    return render(request, "perfil/index.html", {"usuarios": usuarios})

def crear_publicacion(request):
    publicaciones = Publicacion.objects.all()
    form_publicacion = PublicacionForm(request.POST or None, request.FILES or None) #Esto indentifica los elementos de la publicacion y se los asigna a la variable. 
    # request.FILES se pone para cuando vamos a recibir archivos, como una foto o un PDF
    
    if form_publicacion.is_valid():
        form_publicacion.save()
        return redirect("crear_publicacion")
    
    return render(request, "perfil/crear_publicacion.html", {"form_publicacion": form_publicacion, "publicaciones": publicaciones})

def editar_publicacion(request,id):
    publicacion = Publicacion.objects.get(id_publicacion = id)
    form_publicacion = PublicacionForm(request.POST or None, request.FILES or None, instance = publicacion)
    return render(request, "perfil/editar_publicacion.html", {"form_publicacion": form_publicacion})

def eliminar_publicacion(request,id):
    publicacion = Publicacion.objects.get(id_publicacion = id)
    publicacion.delete()
    return redirect("crear_publicacion")
