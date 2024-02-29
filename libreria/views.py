from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from .models import  Publicacion, Comentario, Perfil, Recursos #Importamos las clases
from .forms import PublicacionForm, ComentarioForm, PerfilForm, UserForm, CambiarPasswordForm, RecursosForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
import locale
from datetime import datetime, timedelta
locale.setlocale(locale.LC_ALL, 'es_ES')
perfiles = Perfil.objects.all()

def base(request):
    perfil_usuario = Perfil.objects.get(username_id=request.user.id)
    return render(request, 'base.html', {'perfiles': perfiles ,"perfil_usuario":perfil_usuario})

def inicio(request):
    perfil_usuario = Perfil.objects.get(username_id=request.user.id)
    return render(request, "paginas/inicio.html",{"perfil_usuario":perfil_usuario})

def perfil(request, template_name='perfil/index.html'):
    perfil_usuario = Perfil.objects.get(username_id=request.user.id)
    datos_de_usuario = []
    for perfil in perfiles:
        datos_usuario = {
            'id': perfil.username.id,
            'username': perfil.username.username,
            'full_name': perfil.username.first_name + " " + perfil.username.last_name,
            'profile_pic': perfil.profile_pic.url,
            'last_login': perfil.username.last_login,
            'is_superuser': perfil.username.is_superuser,
            'is_active': perfil.username.is_active,
        }
        datos_de_usuario.append(datos_usuario)

    return render(request, template_name, {"datos_de_usuario": datos_de_usuario, "perfiles": perfiles, "perfil_usuario": perfil_usuario})
    

def editar_perfil(request):
    perfil_usuario = Perfil.objects.get(username=request.user)
    form_user = UserForm(request.POST or None, instance=perfil_usuario.username)
    form_perfil = PerfilForm(request.POST or None, request.FILES or None, instance=perfil_usuario)

    if request.method == 'POST':
        if form_user.is_valid() and form_perfil.is_valid():
            form_user.save()
            form_perfil.save()
            return redirect('ver_perfil', username=request.user.username)  # Redirigir a la página de perfil

    return render(request, "perfil/editar_perfil.html", {"perfil_usuario": perfil_usuario, "form_user": form_user, "form_perfil": form_perfil})




  
           
           
class CambiarPassword(View):
    template_name = "perfil/cambiar_password.html"
    form_password = CambiarPasswordForm
    success_url = reverse_lazy('perfil')
    
    
    def get(self, request):
        perfil_usuario = Perfil.objects.get(username_id=request.user.id)
        return render(request, self.template_name, {'form': self.form_password, 'user': request.user, "perfil_usuario": perfil_usuario})

    def post(self, request):
        perfil_usuario = Perfil.objects.get(username_id=request.user.id)
        form = self.form_password(request.POST)
        if form.is_valid():
            user = User.objects.filter(username=request.user)
            if user.exists():
                user = user.first()
                user.set_password(form.cleaned_data['password1'])
                user.save()
                
                # Reautenticar al usuario después de cambiar la contraseña
                new_user = authenticate(username=user.username, password=form.cleaned_data['password1'])
                if new_user is not None:
                    login(request, new_user)
                    
                return redirect('ver_perfil', username=user.username)
            else:
             return render(request, self.template_name, {'form': form})
        return render(request, self.template_name, {'form': form, 'user': request.user,"perfil_usuario": perfil_usuario})


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
        return redirect("feed")
    return render(request, "perfil/editar_publicacion.html", {"form_publicacion": form_publicacion,'perfiles': perfiles})

def editar_comentario(request, id):
    comentario = Comentario.objects.get(id=id)
    publicacion = Publicacion.objects.get(id=comentario.publicacion_id)
    form_comentario = ComentarioForm(request.POST or None, instance=comentario)  # Pasar la instancia del comentario a editar
    if request.method == 'POST':
        if form_comentario.is_valid() and request.POST:
            form_comentario.save()  # El formulario ya contiene el comentario a editar, no es necesario modificarlo manualmente
            return redirect("feed")
    return render(request, "perfil/editar_comentario.html", {"form_comentario": form_comentario, "publicacion": publicacion, "perfiles": perfiles})



   

def eliminar_publicacion(request,id):
    publicacion = Publicacion.objects.get(id = id)
    publicacion.delete()
    return redirect("listado_publicaciones")

def eliminar_comentario(request,id):
    comentario = Comentario.objects.get(id = id)
    comentario.delete()
    return redirect("feed")

def ver_publicaciones(request, template_name):
    
    publicaciones = Publicacion.objects.all()
    comentarios = Comentario.objects.all()  # Obtener todos los comentarios de la publicación específica
    perfil_usuario = Perfil.objects.get(username_id=request.user.id)

    # Formatear la fecha actual
    ahora = datetime.now().date()


    # Calcular la diferencia en días para cada comentario
    for comentario in comentarios:
        diferencia = ahora - comentario.fecha_publicacion_comentario
        if diferencia.days == 0:
            comentario.dias_desde_publicacion = "hoy"
        elif diferencia.days == 1:
            comentario.dias_desde_publicacion = "ayer"
        else:
            comentario.dias_desde_publicacion = diferencia.days  # Obtener la diferencia en días

    # Obtener el número de comentarios por publicación y formatear la fecha de publicación de la publicación
    for publicacion in publicaciones:
        publicacion.numero_de_comentarios = publicacion.comentarios.count()
        publicacion.fecha_publicacion = publicacion.fecha_publicacion.strftime("%d de %B de %Y")
    return render(request, template_name, {"publicaciones": publicaciones, "perfiles": perfiles,"comentarios": comentarios,"perfil_usuario": perfil_usuario})


def ver_comentarios(request, id):
    publicacion = Publicacion.objects.get(id=id)
    comentarios = publicacion.comentarios.all()  # Obtener todos los comentarios de la publicación específica
    return render(request, "perfil/ver_comentarios.html", {"publicacion": publicacion, "comentarios": comentarios,'perfiles': perfiles})






def ver_perfil(request, username):
    perfil_usuario = Perfil.objects.get(username=request.user) 
    # Obtener el usuario correspondiente al nombre de usuario
    usuario = User.objects.get(username=username)
    # Filtrar las publicaciones por el usuario
    publicaciones = Publicacion.objects.filter(user_id=usuario.id)

    return render(request, "perfil/ver_perfil.html", {"perfil_usuario":perfil_usuario,"publicaciones": publicaciones, "perfiles": perfiles, "usuario": usuario})

def agregar_comentario(request, id):
    publicacion = Publicacion.objects.get(id=id)
    form_comentario = ComentarioForm(request.POST)  # Initialize the form
    if request.method == 'POST':
        if form_comentario.is_valid():
            comentario = form_comentario.save(commit=False)
            comentario.publicacion_id = publicacion.id
            comentario.user_id = request.user.id
            comentario.save()
            return redirect("feed")
    return render(request, "perfil/agregar_comentario.html", {"form_comentario": form_comentario, "publicacion": publicacion,'perfiles': perfiles})

def recursos(request):
    recursos = Recursos.objects.all()
    perfil_usuario = Perfil.objects.get(username_id=request.user.id)
    
    for recurso in recursos:
        # Obtener la extensión del archivo recurso
        extension = recurso.archivo_recurso.name.split(".")[-1]
        # Asignar la extensión al recurso actual
        recurso.extension = extension
    
    return render(request, "perfil/recursos.html", {"recursos": recursos, "perfil_usuario": perfil_usuario})
def agregar_recurso(request):
    recursos = Recursos.objects.all()
    form_recurso = RecursosForm(request.POST, request.FILES)

    
    if request.method == 'POST':
        if form_recurso.is_valid():
            recurso = form_recurso.save(commit=False)
            recurso.save()
            return redirect("recursos")
        else:
            form_recurso = RecursosForm()
  
    fechas_formateadas = [recurso.fecha_publicacion_recurso.strftime("%d de %B de %Y") for recurso in recursos]
    
    return render(request, "perfil/agregar_recurso.html", {"form_recurso": form_recurso, "recursos": recursos, "perfiles": perfiles, "fechas_formateadas": fechas_formateadas})

def eliminar_recurso(request,id):
    recurso = Recursos.objects.get(id = id)
    recurso.delete()
    return redirect("agregar_recurso")