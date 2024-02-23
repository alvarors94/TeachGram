from django.shortcuts import render, redirect
from .models import  Publicacion, Comentario, Perfil #Importamos las clases
from .forms import PublicacionForm, ComentarioForm
from django.contrib.auth.models import User

perfiles = Perfil.objects.all()

def base(request):
    return render(request, 'base.html', {'perfiles': perfiles})

def inicio(request):
    return render(request, "paginas/inicio.html",{'perfiles': perfiles})

def perfil(request):

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
            return redirect("listado_publicaciones")
    else:
        form_publicacion = PublicacionForm()
    
    return render(request, "perfil/crear_publicacion.html", {"form_publicacion": form_publicacion,'perfiles': perfiles})

def editar_publicacion(request,id):
    publicacion = Publicacion.objects.get(id = id)
    form_publicacion = PublicacionForm(request.POST or None, request.FILES or None, instance = publicacion)
    if form_publicacion.is_valid() and request.POST:
        form_publicacion.save()
        return redirect("listado_publicaciones")
    return render(request, "perfil/editar_publicacion.html", {"form_publicacion": form_publicacion,'perfiles': perfiles})

def eliminar_publicacion(request,id):
    publicacion = Publicacion.objects.get(id = id)
    publicacion.delete()
    return redirect("listado_publicaciones")

def ver_publicaciones(request, template_name):
    publicaciones = Publicacion.objects.all()
    comentarios = Comentario.objects.all()  # Obtener todos los comentarios de la publicación específica
    for publicacion in publicaciones:
        publicacion.numero_de_comentarios = publicacion.comentarios.count()
    return render(request, template_name, {"publicaciones": publicaciones, "perfiles": perfiles, "comentarios": comentarios})



def ver_comentarios(request, id):
    publicacion = Publicacion.objects.get(id=id)
    comentarios = publicacion.comentarios.all()  # Obtener todos los comentarios de la publicación específica
    return render(request, "perfil/ver_comentarios.html", {"publicacion": publicacion, "comentarios": comentarios,'perfiles': perfiles})




def ver_perfil(request, username):
    # Obtener el usuario correspondiente al nombre de usuario
    usuario = User.objects.get(username=username)
    # Filtrar las publicaciones por el usuario
    publicaciones = Publicacion.objects.filter(user_id=usuario.id)

    return render(request, "perfil/ver_perfil.html", {"publicaciones": publicaciones, "perfiles": perfiles, "usuario": usuario})


def editar_perfil(request, username):
    publicaciones = Publicacion.objects.all()
    # publicaciones = Publicacion.objects.filter(usuario__username=username)
    # Obtener todos los comentarios de la publicación específica
    return render(request, "perfil/ver_perfil.html", {"publicaciones": publicaciones, "perfiles": perfiles})

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
    return render(request, "perfil/agregar_comentario.html", {"form_comentario": form_comentario, "publicacion": publicacion,'perfiles': perfiles})
