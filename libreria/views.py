from django.shortcuts import render, redirect
from .models import Usuario, Publicacion, Comentario #Importamos las clases
from .forms import PublicacionForm, ComentarioForm
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
        return redirect("publicaciones")
    
    return render(request, "perfil/crear_publicacion.html", {"form_publicacion": form_publicacion, "publicaciones": publicaciones})

def editar_publicacion(request,id):
    publicacion = Publicacion.objects.get(id_publicacion = id)
    form_publicacion = PublicacionForm(request.POST or None, request.FILES or None, instance = publicacion)
    if form_publicacion.is_valid() and request.POST:
        form_publicacion.save()
        return redirect("crear_publicacion")
    return render(request, "perfil/editar_publicacion.html", {"form_publicacion": form_publicacion})

def eliminar_publicacion(request,id):
    publicacion = Publicacion.objects.get(id_publicacion = id)
    publicacion.delete()
    return redirect("crear_publicacion")

def ver_publicaciones(request):
    publicaciones = Publicacion.objects.all()
    return render(request, "perfil/publicaciones.html", {"publicaciones": publicaciones})

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
            comentario.publicacion_id = publicacion.id_publicacion  # Asignar el ID de la publicación al comentario
            comentario.save()
            return redirect("publicaciones")
    else:
        form_comentario = ComentarioForm(initial={'publicacion': publicacion.id_publicacion})  # Inicializar el formulario con el ID de la publicación
    return render(request, "perfil/agregar_comentario.html", {"form_comentario": form_comentario, "publicacion": publicacion})

