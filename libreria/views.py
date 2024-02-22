from django.shortcuts import render, redirect
from .models import  Publicacion, Comentario, Perfil #Importamos las clases
from .forms import PublicacionForm, ComentarioForm
from django.contrib.auth import logout

def base(request):
    perfiles = Perfil.objects.first()  # Aquí asumo que estás obteniendo el primer perfil de la base de datos
    return render(request, 'base.html', {'perfiles': perfiles})

def inicio(request):
    return render(request, "paginas/inicio.html")

def perfil(request):
    # Obtener todos los perfiles
    perfiles = Perfil.objects.all()

    # Crear una lista para almacenar los nombres de usuario y otros atributos
    datos_de_usuario = []

    # Iterar sobre cada perfil y obtener los datos del usuario
    for perfil in perfiles:
        # Crear un diccionario para almacenar los datos del usuario
        datos_usuario = {
            'id': perfil.username.id,
            'username': perfil.username.username,  # Nombre de usuario
            'full_name': perfil.full_name,
            'profile_pic': perfil.profile_pic.url,
            'last_login': perfil.username.last_login,  
            'is_superuser': perfil.username.is_superuser,
            'is_active': perfil.username.is_active,
            # Otros atributos del modelo User que desees incluir
        }
        # Añadir los datos del usuario a la lista
        datos_de_usuario.append(datos_usuario)

    return render(request, "perfil/index.html", {"datos_de_usuario": datos_de_usuario, "perfiles": perfiles})

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
    publicacion = Publicacion.objects.get(id = id)
    form_publicacion = PublicacionForm(request.POST or None, request.FILES or None, instance = publicacion)
    if form_publicacion.is_valid() and request.POST:
        form_publicacion.save()
        return redirect("publicaciones")
    return render(request, "perfil/editar_publicacion.html", {"form_publicacion": form_publicacion})

def eliminar_publicacion(request,id):
    publicacion = Publicacion.objects.get(id = id)
    publicacion.delete()
    return redirect("publicaciones")

def ver_publicaciones(request):
    publicaciones = Publicacion.objects.all()
    perfiles = Perfil.objects.all()
    return render(request, "perfil/publicaciones.html", {"publicaciones": publicaciones, "perfiles": perfiles})


def ver_comentarios(request, id):
    publicacion = Publicacion.objects.get(id=id)
    comentarios = publicacion.comentarios.all()  # Obtener todos los comentarios de la publicación específica
    return render(request, "perfil/ver_comentarios.html", {"publicacion": publicacion, "comentarios": comentarios})

def agregar_comentario(request, id):
    publicacion = Publicacion.objects.get(id=id)
    form_comentario = ComentarioForm(request.POST)  # Initialize the form
    if request.method == 'POST':
        if form_comentario.is_valid():
            comentario = form_comentario.save(commit=False)
            comentario.publicacion_id = publicacion.id
            comentario.user_id = request.user.id
            comentario.save()
            return redirect("publicaciones")
    return render(request, "perfil/agregar_comentario.html", {"form_comentario": form_comentario, "publicacion": publicacion})
