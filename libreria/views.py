from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from .models import  Publicacion, Comentario, Perfil, Recursos, Imagen, Iframe #Importamos las clases
from .forms import PublicacionForm, ComentarioForm, PerfilForm, UserForm, CambiarPasswordForm, RecursosForm, forms, IframeForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
import locale
from datetime import datetime, timedelta
import re
import os
from django.conf import settings
locale.setlocale(locale.LC_ALL, 'es_ES')
perfiles = Perfil.objects.all()


def base(request):
    user = User.objects.get(id=request.user.id)
    foto_perfil = user.perfil.profile_pic
    return render(request, 'base.html', {"foto_perfil":foto_perfil})

def inicio(request):
    user = User.objects.get(id=request.user.id)
    foto_perfil = user.perfil.profile_pic
    return render(request, "paginas/inicio.html",{ "foto_perfil":foto_perfil})

def listado_perfiles(request, template_name='perfil/listado_perfiles.html'):
    publicaciones = Publicacion.objects.all()
    comentarios = Comentario.objects.all()
    
    datos_de_user = []  # Inicializa una lista vacía fuera del bucle

    users = User.objects.all()
    for user in users:
        perfil = Perfil.objects.get(id=user.id)
        last_login = user.last_login
        if last_login is not None:
            last_login = last_login + timedelta(hours=1)  # Sumar una hora al tiempo de inicio de sesión
            last_login_str = last_login.strftime("%d/%m/%Y - %H:%M:%S")
        else:
            last_login_str = "No ha accedido aún"
        
        # Crea un diccionario para cada usuario y agrégalo a la lista
        datos_usuario = {
            'id': user.id,
            'username': user.username,
            'full_name': user.get_full_name(),
            'profile_pic': perfil.profile_pic,  # Accede al campo profile_pic a través del objeto Perfil
            'last_login': last_login_str,
            'is_superuser': user.is_superuser,
            'is_active': user.is_active,
            'is_blocked': perfil.is_blocked,  # Accede al campo is_blocked a través del objeto Perfil
            'total_comentarios': Comentario.objects.filter(user_id=user.id).count(),
            'total_publicaciones': Publicacion.objects.filter(user_id=user.id).count(),
        }
        datos_de_user.append(datos_usuario)  # Agrega el diccionario a la lista

    return render(request, template_name, {"datos_de_user":datos_de_user,"comentarios":comentarios,"publicaciones":publicaciones,"perfiles": perfiles})
    


class CambiarPassword(View):
    template_name = "perfil/cambiar_password.html"
    form_password = CambiarPasswordForm
    success_url = reverse_lazy('perfil')
    
    def get(self, request):
        return render(request, self.template_name, {'form': self.form_password, 'user': request.user})

    def post(self, request):
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
        return render(request, self.template_name, {'form': form, 'user': request.user})


def crear_publicacion(request):
    form_publicacion = PublicacionForm()  # Definir form_publicacion fuera del bloque de condición

    if request.method == 'POST':
        form_publicacion = PublicacionForm(request.POST, request.FILES)
        
        if form_publicacion.is_valid():
            publicacion = form_publicacion.save(commit=False)
            publicacion.user_id = request.user.id  # Asigna el id del usuario autenticado
            publicacion.save()

            images = request.FILES.getlist('images')
            # Recorrer la lista de archivos adjuntos,
            for image in images:
                Imagen.objects.create(imagen=image, publicacion_id=publicacion.id)
    
            return redirect("feed")
    
    return render(request, "perfil/crear_publicacion.html", {"form_publicacion": form_publicacion})


def editar_publicacion(request, id):
    publicacion = Publicacion.objects.get(id=id)
    imagenes_publicacion = Imagen.objects.filter(publicacion_id=publicacion.id)
    form_publicacion = PublicacionForm(request.POST or None, request.FILES or None, instance=publicacion)
    
    
    if request.method == 'POST':
        if form_publicacion.is_valid():
            form_publicacion.save()
            images = request.FILES.getlist('images')
            for image in images:
                Imagen.objects.create(imagen=image, publicacion_id=publicacion.id)

            return redirect(reverse('ver_perfil', kwargs={'username': publicacion.user.username}))
            
    return render(request, "perfil/editar_publicacion.html", {"form_publicacion": form_publicacion, 'perfiles': perfiles, "imagenes_publicacion": imagenes_publicacion})

        
    
#     return render(request, "perfil/crear_publicacion.html", {"form_publicacion": form_publicacion})
def editar_comentario(request, id):
    comentario = Comentario.objects.get(id=id)
    publicacion = Publicacion.objects.get(id=comentario.publicacion_id)
    form_comentario = ComentarioForm(request.POST or None, instance=comentario)  # Pasar la instancia del comentario a editar
    usuario_publicacion = publicacion.user
    if request.method == 'POST':
        if form_comentario.is_valid() and request.POST:
            form_comentario.save()  # El formulario ya contiene el comentario a editar, no es necesario modificarlo manualmente

        if 'perfil' in request.META.get('HTTP_REFERER', ''):
                # Si estaba en la página de feed, redirigir de vuelta a esa página
                return redirect(reverse('ver_perfil', kwargs={'username': usuario_publicacion.username}))
            
            # De lo contrario, redirigir a la página de perfil del usuario que publicó la publicación
        return redirect('feed')
        
        # De lo contrario, redirigir a la página de perfil del usuario que publicó la publicación
    return redirect('feed')

def bloquear_perfil(request, id):
    # Obtener el usuario y su perfil asociado
    perfil = Perfil.objects.get(username_id=id)
    # Cambiar el estado de is_blocked
    perfil.is_blocked = not perfil.is_blocked  # Invierte el valor actual
    # Guardar los cambio
    perfil.save()
    return redirect('listado_perfiles')

def hacer_superusuario(request, id):
    # Obtener el usuario y su perfil asociado
    usuario = User.objects.get(id=id)
    # Cambiar el estado de is_blocked
    usuario.is_superuser = not usuario.is_superuser  # Invierte el valor actual
    # Guardar los cambio
    usuario.save()
    return redirect('listado_perfiles')

def eliminar_publicacion(request, id):
    publicacion = Publicacion.objects.get(id=id)
    usuario_publicacion = publicacion.user
    
    # Eliminar todas las imágenes asociadas a la publicación
    imagenes = publicacion.imagenes.all()
    for imagen in imagenes:
        imagen_path = os.path.join(settings.MEDIA_ROOT, str(imagen.imagen))
        if os.path.exists(imagen_path):
            os.remove(imagen_path)
        imagen.delete()

    # Eliminar la publicación
    publicacion.delete()

    if 'perfil' in request.META.get('HTTP_REFERER', ''):
        # Si estaba en la página de feed, redirigir de vuelta a esa página
        return redirect(reverse('ver_perfil', kwargs={'username': usuario_publicacion.username}))
    elif 'listado_publicaciones' in request.META.get('HTTP_REFERER', ''):
        # Si estaba en la página de feed, redirigir de vuelta a esa página
        return redirect("listado_publicaciones")
        
    # De lo contrario, redirigir a la página de perfil del usuario que publicó la publicación
    return redirect('feed')

def eliminar_perfil(request, id):
    usuario = User.objects.get(id=id)
    usuario.delete()
    return redirect('listado_perfiles')

def eliminar_comentario(request,id):
    comentario = Comentario.objects.get(id = id)
    publicacion = Publicacion.objects.get(id=comentario.publicacion_id)
    usuario_publicacion = publicacion.user
    comentario.delete()
    if 'perfil' in request.META.get('HTTP_REFERER', ''):
        # Si estaba en la página de feed, redirigir de vuelta a esa página
        return redirect(reverse('ver_perfil', kwargs={'username': usuario_publicacion.username}))
    elif 'listado_publicaciones' in request.META.get('HTTP_REFERER', ''):
        # Si estaba en la página de feed, redirigir de vuelta a esa página
        return redirect("listado_publicaciones")
        
    # De lo contrario, redirigir a la página de perfil del usuario que publicó la publicación
    return redirect('feed')


def eliminar_imagen(request, id):
    imagen = Imagen.objects.get(id=id)
    # Obtiene la ruta completa de la imagen en el directorio de medios
    imagen_path = os.path.join(settings.MEDIA_ROOT, str(imagen.imagen))
    # Elimina la imagen del directorio
    if os.path.exists(imagen_path):
        os.remove(imagen_path)
    # Elimina la entrada de imagen de la base de datos
    imagen.delete()
    return redirect(reverse_lazy("editar_publicacion", kwargs={'id': imagen.publicacion_id}))

    
def ver_publicaciones(request, template_name):
    imagenes = Imagen.objects.all()
    publicaciones = Publicacion.objects.all()
    comentarios = Comentario.objects.all()  # Obtener todos los comentarios de la publicación específica

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
    return render(request, template_name, {"imagenes":imagenes,"publicaciones": publicaciones, "perfiles": perfiles,"comentarios": comentarios})



def ver_perfil(request, username):
    user = User.objects.get(username=username)
    foto_de_perfil = user.perfil.profile_pic
    ahora = datetime.now().date()
    # Obtener el usuario correspondiente al nombre de usuario
    
    # Filtrar las publicaciones por el usuario
    publicaciones = Publicacion.objects.filter(user_id=user.id)
    comentarios = Comentario.objects.all()
    imagenes = Imagen.objects.all()
    for publicacion in publicaciones:
        publicacion.fecha_publicacion=publicacion.fecha_publicacion.strftime("%d de %B de %Y")
        
    for comentario in comentarios:
        diferencia = ahora - comentario.fecha_publicacion_comentario
        if diferencia.days == 0:
            comentario.dias_desde_publicacion = "hoy"
        elif diferencia.days == 1:
            comentario.dias_desde_publicacion = "ayer"
        else:
            comentario.dias_desde_publicacion = diferencia.days  # Obtener la diferencia en días

    return render(request, "perfil/ver_perfil.html", {"publicaciones": publicaciones, "perfiles": perfiles, "user": user, "imagenes": imagenes, "comentarios":comentarios, "foto_de_perfil":foto_de_perfil})

def agregar_comentario(request, id):
    if request.method == 'POST':
        publicacion = Publicacion.objects.get(id=id)
        form_comentario = ComentarioForm(request.POST)
        if form_comentario.is_valid():
            comentario = form_comentario.save(commit=False)
            comentario.publicacion = publicacion
            comentario.user = request.user
            comentario.save()
            
            # Obtener el usuario asociado a la publicación
            usuario_publicacion = publicacion.user
            
            if 'perfil' in request.META.get('HTTP_REFERER', ''):
        # Si estaba en la página de feed, redirigir de vuelta a esa página
                 return redirect(reverse('ver_perfil', kwargs={'username': usuario_publicacion.username}))
            elif 'listado_publicaciones' in request.META.get('HTTP_REFERER', ''):
                # Si estaba en la página de feed, redirigir de vuelta a esa página
                return redirect("listado_publicaciones")
        
    # De lo contrario, redirigir a la página de perfil del usuario que publicó la publicación
    return redirect('feed')
    
    
                        
def crear_usuario(request):

    form_usuario = UserForm()
    form_perfil = PerfilForm()
    
    if request.method == 'POST':
        form_usuario = UserForm(request.POST)
        form_perfil = PerfilForm(request.POST)
        if form_usuario.is_valid() and form_perfil.is_valid():
            usuario = form_usuario.save(commit=False)
            password = request.POST.get('password')  # Obtener la contraseña del formulario
            usuario.set_password(password)
            perfil = form_perfil.save(commit=False)
            perfil.is_staff = False
            perfil.is_blocked = False
            usuario.save()
            perfil.user = usuario  # Asignar el usuario al perfil
            perfil.id = usuario.id
            perfil.username_id = usuario.id
            perfil.save()
            # Aquí verificar si se ha enviado el campo de superusuario en el formulario
            if 'superusuario' in request.POST:
                usuario.is_superuser = True  # O False si deseas desactivarlo
                usuario.save()
                
            return redirect("feed")
    else:
        form_usuario = UserForm()  # Inicializar el formulario sin datos
        form_perfil = PerfilForm()  # Inicializar el formulario sin datos
    
    return render(request, "perfil/crear_usuario.html", {"form_usuario": form_usuario, "form_perfil": form_perfil})

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']  # Excluir 'password' del formulario
        labels = {
            'username': 'Nombre de usuario',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
        }
        
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

def editar_perfil(request):
    perfil_usuario = Perfil.objects.get(username=request.user)

    if request.method == 'POST':
        form_user = UserForm(request.POST, instance=request.user)
        form_perfil = PerfilForm(request.POST, request.FILES, instance=perfil_usuario)
        if form_user.is_valid() and form_perfil.is_valid():
            form_user.save()
            form_perfil.save()
            return redirect('feed')  # Redirigir a la página de perfil
    else:
        form_user = UserForm(instance=request.user)
        form_perfil = PerfilForm(instance=perfil_usuario)

    return render(request, "perfil/editar_perfil.html", {"form_user": form_user, "form_perfil": form_perfil})


def recursos(request):
    recursos = Recursos.objects.all()
    iframes = Iframe.objects.all()
    src_value = ""
    
    for recurso in recursos:
        # Obtener la extensión del archivo recurso
        extension = recurso.archivo_recurso.name.split(".")[-1]
        # Asignar la extensión al recurso actual
        recurso.extension = extension
        recurso.fecha_publicacion_recurso = recurso.fecha_publicacion_recurso.strftime("%d de %B de %Y")
   
    
        if iframes:  # Verifica si hay registros de iframes
            # Modifica cada iframe para extraer solo el contenido del atributo src y convertir el código a mayúsculas
            for iframe in iframes:
                codigo = iframe.codigo_iframe
                
                # Utiliza una expresión regular para encontrar el valor de src en el código del iframe
                match = re.search(r'src="([^"]+)"', codigo)
                
                # Verifica si se encontró un match y obtiene el contenido de src en minúsculas
                if match:
                    src_value = match.group(1)
                    iframe.codigo_iframe = src_value  # Actualiza el código del iframe
                else:
                    print("No hay coincidencias")
    
    return render(request, "perfil/recursos.html", {"recursos": recursos, "perfiles": perfiles, "iframes": iframes, "src_value": src_value})

def agregar_recurso(request):
    recursos = Recursos.objects.all()
   
    form_recurso = RecursosForm()
    
    if request.method == 'POST':
        form_recurso = RecursosForm(request.POST, request.FILES)
        
        if form_recurso.is_valid():
            recurso = form_recurso.save(commit=False)
            recurso.save()
        
    
    for recurso in recursos:
        recurso.fecha_publicacion_recurso = recurso.fecha_publicacion_recurso.strftime("%d de %B de %Y")
    
    return render(request, 'perfil/agregar_recurso.html', {"form_recurso": form_recurso,"recursos": recursos})

def agregar_recurso_externo(request):
    recursos_externos = Iframe.objects.all()
    if request.method == 'POST':
        form_recurso_externo = IframeForm(request.POST)
        if form_recurso_externo.is_valid():
            form_recurso_externo.save()
            return redirect('recursos')
    else:
        form_recurso_externo = IframeForm()

    return render(request, 'perfil/agregar_recurso_externo.html', {"form_recurso_externo": form_recurso_externo, "recursos_externos":recursos_externos})

def eliminar_recurso_externo(request,id):
    recurso_externo = Iframe.objects.get(id = id)
    recurso_externo.delete()
    return redirect("recursos")

def eliminar_recurso(request,id):
    recurso = Recursos.objects.get(id = id)
    recurso.delete()
    return redirect("recursos")

def editar_recurso(request,id):
    recurso = Recursos.objects.get(id = id)
    form_recurso = RecursosForm(request.POST or None, request.FILES or None, instance = recurso)
    if form_recurso.is_valid() and request.POST:
        form_recurso.save()
        return redirect("agregar_recurso")
    return render(request, "perfil/editar_recurso.html", {"form_recurso": form_recurso,'perfiles': perfiles, "recurso": recurso})

def editar_recurso_externo(request,id):
    recurso_externo = Iframe.objects.get(id = id)
    form_recurso_externo = IframeForm(request.POST or None, instance = recurso_externo)
    if form_recurso_externo.is_valid() and request.POST:
        form_recurso_externo.save()
        return redirect("recursos")
    return render(request, "perfil/editar_recurso_externo.html", {"form_recurso_externo": form_recurso_externo, "recurso_externo": recurso_externo})


