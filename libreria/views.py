from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from .models import  Publicacion, Comentario, Perfil, Recursos, Imagen, Iframe
from .forms import PublicacionForm, ComentarioForm, PerfilForm, UserForm, CambiarPasswordForm, RecursosForm, IframeForm, EditarPerfilForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
import locale, re, os
from datetime import datetime, timedelta
from django.conf import settings

locale.setlocale(locale.LC_ALL, 'es_ES')
perfiles = Perfil.objects.all()

@login_required
def base(request):
    '''
    Renderiza la página de base.html

    Parámteros:
    - request (HttpRequest): El objeto HTTP de request.

    Returns:
    - HttpResponse: La plantilla base.html renderizada.'''
    user = User.objects.get(id=request.user.id)
    return render(request, 'base.html')

@login_required
def crear_usuario(request):
    """
    Crea un nuevo usuario y su perfil asociado.

    Este método maneja tanto la solicitud GET como POST. En una solicitud GET, se presentan formularios vacíos para crear un nuevo usuario y perfil. 
    En una solicitud POST, se procesan los datos del formulario enviado para crear un nuevo usuario y perfil. Si los formularios son válidos, se establece la contraseña del usuario, se guardan el usuario y el perfil en la base de datos, y se redirige al usuario a la página de 'feed'.

    Parámetros:
    - request (HttpRequest): La solicitud HTTP enviada al servidor.

    Retorna:
    - HttpResponse: Una respuesta HTTP que renderiza 'perfil/crear_usuario.html' con los formularios de usuario y perfil en el contexto, o redirige a la página de 'feed' después de crear el usuario y perfil con éxito.
    """
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
                usuario.is_superuser = True  
                usuario.save()
            
            # Verificar si el usuario ya tiene un perfil asociado
            if not Perfil.objects.filter(username_id=usuario.id).exists():
                nuevo_perfil = Perfil(username_id=usuario.id)
                nuevo_perfil.save()
                
            return redirect("feed")
    else:
        form_usuario = UserForm()  # Inicializar el formulario sin datos
        form_perfil = PerfilForm()  # Inicializar el formulario sin datos
    
    return render(request, "perfil/crear_usuario.html", {"form_usuario": form_usuario, "form_perfil": form_perfil})


@login_required
def listado_perfiles(request, template_name='perfil/listado_perfiles.html'):
        """
    Genera un listado de perfiles de usuario, incluyendo información detallada de cada uno.

    Esta función recopila información de todos los usuarios, sus perfiles, publicaciones y comentarios.
    Para cada usuario, se prepara un diccionario con datos como el nombre de usuario, nombre completo,
    foto de perfil, última conexión, si es superusuario, si está activo, si está bloqueado, si es staff,
    total de comentarios realizados y total de publicaciones. Esta información se pasa al template especificado.

    Parámetros:
    - request (HttpRequest): La solicitud HTTP enviada al servidor.
    - template_name: String que especifica el nombre del template a utilizar.

    Retorna:
    - HttpResponse con el 'template' renderizado y el contexto que incluye los datos de los usuarios,
      comentarios, publicaciones y perfiles.
    """
        publicaciones = Publicacion.objects.all()
        comentarios = Comentario.objects.all()
        
        datos_de_user = []  # Inicializa una lista vacía fuera del bucle

        users = User.objects.all()
        for user in users:
            perfil = Perfil.objects.get(username_id=user.id)
            last_login = user.last_login
            if last_login is not None:
                last_login = last_login + timedelta(hours=1)  # Sumar una hora al tiempo de inicio de sesión
                last_login_str = last_login.strftime("%d/%m/%Y - %H:%M:%S")
            else:
                last_login_str = "No ha accedido aún"
            
           
            datos_usuario = {
                'id': user.id,
                'username': user.username,
                'full_name': user.get_full_name(),
                'profile_pic': perfil.profile_pic,  
                'last_login': last_login_str,
                'is_superuser': user.is_superuser,
                'is_active': user.is_active,
                'is_blocked': perfil.is_blocked,  
                'is_staff': perfil.is_staff, 
                'total_comentarios': Comentario.objects.filter(user_id=user.id).count(),
                'total_publicaciones': Publicacion.objects.filter(user_id=user.id).count(),
            }
            datos_de_user.append(datos_usuario)  

        return render(request, template_name, {"datos_de_user":datos_de_user,"comentarios":comentarios,"publicaciones":publicaciones,"perfiles": perfiles})
    

class CambiarPassword(View):
    """
    Clase para permitir a los usuarios cambiar su contraseña.

    Esta vista maneja tanto la solicitud GET para mostrar el formulario de cambio de contraseña,
    como la solicitud POST para procesar el formulario. Si el formulario es válido, actualiza la contraseña
    del usuario, lo reautentica y redirige al perfil del usuario.

    Atributos:
        template_name (str): El nombre del template utilizado para mostrar el formulario.
        form_password (Form): El formulario utilizado para el cambio de contraseña.
        success_url (str): URL a la que se redirige al usuario después de un cambio de contraseña exitoso.
    """
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

@login_required
def crear_publicacion(request):
    """
    Función que crea una nueva publicación en la plataforma.

    Este método maneja la solicitud de creación de una nueva publicación por parte de un usuario autenticado.
    Inicializa un formulario de publicación vacío y, en caso de recibir una solicitud POST con datos válidos,
    guarda la nueva publicación en la base de datos. También maneja la carga y asociación de imágenes a la publicación.

    Parámetros:
    - request:Objeto HttpRequest
        La solicitud HTTP enviada al servidor. Contiene los datos de la publicación y las imágenes asociadas, si las hay.

    Retorna:
    - HttpResponse
        Una respuesta HTTP que redirige al usuario al feed principal si la publicación se crea con éxito,
        o vuelve a mostrar el formulario de creación con errores de validación si los hay.
    """
    form_publicacion = PublicacionForm()  

    if request.method == 'POST':
        form_publicacion = PublicacionForm(request.POST, request.FILES)
        
        if form_publicacion.is_valid():
            publicacion = form_publicacion.save(commit=False)
            publicacion.user_id = request.user.id  # Asigna el id del usuario autenticado
            publicacion.save()

            images = request.FILES.getlist('images')
            for image in images:
                Imagen.objects.create(imagen=image, publicacion_id=publicacion.id)
    
            return redirect("feed")
    
    return render(request, "perfil/crear_publicacion.html", {"form_publicacion": form_publicacion})

@login_required
def editar_publicacion(request, id):
    '''
    Función encargada de editar una publicación existente.

    Esta función permite editar una publicación existente en el sistema. El usuario debe estar autenticado para acceder a esta funcionalidad. Se espera que se le pase el ID de la publicación como parámetro.

    Parámetros:
    - request: La solicitud HTTP recibida.
    - id: El ID de la publicación a editar.

    Retorna:
    - Si la solicitud es GET, se renderiza la plantilla 'perfil/editar_publicacion.html' con el formulario de edición de la publicación, la publicación y las imágenes asociadas.
    - Si la solicitud es POST y el formulario es válido, se guarda la publicación editada y se crean las nuevas imágenes asociadas. Luego, se redirige al perfil del usuario que realizó la publicación.
    '''
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
            
    return render(request, "perfil/editar_publicacion.html", {"form_publicacion": form_publicacion, "publicacion": publicacion, "imagenes_publicacion": imagenes_publicacion})

        
    
@login_required
def editar_comentario(request, id):
    """
    Edita un comentario. 
    Esta función permite a un usuario logueado editar un comentario. Recupera el objeto comentario basado en el ID proporcionado y la publicación asociada. 
    El formulario muestra el comentario con los datos existentes del comentario para su edición. Si el formulario es válido y el método de solicitud es POST, el comentario actualizado se guarda.
    
    Parámetros:
    - request (HttpRequest): El objeto de solicitud HTTP.
    - id (int): El ID del comentario a editar.
    
    Retorna:
    - HttpResponseRedirect: Si el formulario es válido y el método de solicitud es POST, el usuario es redirigido a la página apropiada:
        - Si el usuario estaba en la página de perfil, se le redirige de vuelta a la página de perfil del usuario que hizo la publicación.
        - De lo contrario, se le redirige a la página de feed.
    - HttpResponseRedirect: Si el formulario no es válido o el método de solicitud no es POST, el usuario es redirigido a la página de feed.
    """
    comentario = Comentario.objects.get(id=id)
    publicacion = Publicacion.objects.get(id=comentario.publicacion_id)
    form_comentario = ComentarioForm(request.POST or None, instance=comentario)  # Pasar la instancia del comentario a editar
    usuario_publicacion = publicacion.user
    if request.method == 'POST':
        if form_comentario.is_valid() and request.POST:
            form_comentario.save()  

        if 'perfil' in request.META.get('HTTP_REFERER', ''):
                # Si estaba en la página de feed, redirigir de vuelta a esa página
                return redirect(reverse('ver_perfil', kwargs={'username': usuario_publicacion.username}))
            
            # De lo contrario, redirigir a la página de perfil del usuario que publicó la publicación
        return redirect('feed')
        
        
    return redirect('feed')

@login_required
def bloquear_perfil(request, id):
    """
    Cambia el estado de bloqueo de un perfil de usuario.

    Toma como argumentos el `request` y el `id` del usuario cuyo perfil se desea bloquear o desbloquear.
    Obtiene el perfil asociado al `id` proporcionado, invierte el valor de la propiedad `is_blocked` del perfil,
    guarda los cambios y redirige a la vista de 'listado_perfiles'.

    Parámetros:
        request: HttpRequest object.
        id (int): El identificador del usuario cuyo perfil se desea bloquear o desbloquear.

    Retorna:
        HttpResponseRedirect: Redirige a la vista 'listado_perfiles' después de cambiar el estado de bloqueo.
    """
    # Obtener el usuario y su perfil asociado
    perfil = Perfil.objects.get(username_id=id)

    perfil.is_blocked = not perfil.is_blocked  # Invierte el valor actual

    perfil.save()
    return redirect('listado_perfiles')

@login_required
def hacer_superusuario(request, id): 
    """
    Cambia el estado de superusuario de un perfil de usuario.

    Toma como argumentos el `request` y el `id` del usuario cuyo perfil se desea convertir en superusuario o quitar dicho privilegio.
    Obtiene el usuario asociado al `id` proporcionado, invierte el valor de la propiedad `is_superuser` del usuario,
    guarda los cambios y redirige a la vista de 'listado_perfiles'.

    Parámetros:
        request: HttpRequest object.
        id (int): El identificador del usuario cuyo perfil se convertir a superusuario.

    Retorna:
        HttpResponseRedirect: Redirige a la vista 'listado_perfiles' después de cambiar el estado de superusuario.
    """
    # Obtener el usuario y su perfil asociado
    usuario = User.objects.get(id=id)

    usuario.is_superuser = not usuario.is_superuser  # Invierte el valor actual

    usuario.save()
    return redirect('listado_perfiles')

@login_required
def eliminar_publicacion(request, id):
    """
    Elimina una publicación específica junto con todas las imágenes asociadas a ella.

    Primero, busca la publicación por su ID y elimina todas las imágenes relacionadas, borrando
    los archivos de imagen del sistema de archivos. Luego, elimina la publicación de la base de datos.
    Finalmente, redirige al usuario a la página de perfil, al listado de publicaciones o al feed,
    dependiendo de la página de origen.

    Parámetros:
    - request: HttpRequest object, contiene metadatos sobre la solicitud.
    - id: int, el identificador único de la publicación a eliminar.

    Retorna:
    - HttpResponse, redirige al usuario a la página correspondiente después de eliminar la publicación.
    """
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
        
    return redirect('feed')

@login_required
def eliminar_perfil(request, id):
    """
    Elimina el perfil de un usuario y su foto de perfil asociada del sistema.

    Primero, busca el usuario basado en el 'id' proporcionado. Luego, intenta eliminar la foto de perfil
    asociada al usuario del sistema de archivos y de la base de datos. Finalmente, elimina el usuario de la base de datos.
    Si la operación es exitosa, redirige al listado de perfiles.

    Parámetros:
    - request (HttpRequest): La solicitud HTTP enviada al servidor.
    - id (int): El identificador único del usuario a eliminar.

    Retorna:
    - HttpResponseRedirect hacia la vista 'listado_perfiles' después de eliminar el usuario y su foto de perfil.
    """
    usuario = User.objects.get(id=id)
    
    foto_perfil = usuario.perfil.profile_pic
    foto_perfil_path = foto_perfil.path
    
    if os.path.exists(foto_perfil_path):
        os.remove(foto_perfil_path)
    
    foto_perfil.delete()
    usuario.delete()
    return redirect('listado_perfiles')

@login_required
def eliminar_comentario(request,id):
    """
    Elimina un comentario específico basado en su ID. Después de eliminar el comentario,
    redirige al usuario a la página anterior, ya sea el perfil del usuario, el listado de publicaciones,
    o el feed, dependiendo de la página de origen.
    
    Parámetros:
    - request: HttpRequest
    - id: int, el ID del comentario a eliminar.
    
    Retorna:
    - HttpResponseRedirect hacia la vista 'listado_publicaciones' o 'feed' en función de la página donde estuviese
    """
    comentario = Comentario.objects.get(id = id)
    publicacion = Publicacion.objects.get(id=comentario.publicacion_id)
    usuario_publicacion = publicacion.user
    comentario.delete()
    if 'perfil' in request.META.get('HTTP_REFERER', ''):

        return redirect(reverse('ver_perfil', kwargs={'username': usuario_publicacion.username}))
    elif 'listado_publicaciones' in request.META.get('HTTP_REFERER', ''):

        return redirect("listado_publicaciones")
        

    return redirect('feed')

@login_required
def eliminar_imagen(request, id):
    """
    Elimina una imagen específica tanto del directorio de medios como de la base de datos.

    Esta función busca una imagen por su ID, elimina el archivo de imagen del directorio de medios si existe,
    y luego elimina el registro de la imagen de la base de datos. Finalmente, redirige al usuario a la página
    de edición de la publicación asociada a la imagen.

    Parámetros:
    - request: HttpRequest
        La solicitud HTTP enviada al servidor.
    - id: int
        El identificador único de la imagen a eliminar.

    Retorna:
    - HttpResponseRedirect
        Redirección a la página de edición de la publicación asociada a la imagen eliminada.
    """
    imagen = Imagen.objects.get(id=id)
    # Obtiene la ruta completa de la imagen en el directorio de medios
    imagen_path = os.path.join(settings.MEDIA_ROOT, str(imagen.imagen))
    # Elimina la imagen del directorio
    if os.path.exists(imagen_path):
        os.remove(imagen_path)
    # Elimina la entrada de imagen de la base de datos
    imagen.delete()
    return redirect(reverse_lazy("editar_publicacion", kwargs={'id': imagen.publicacion_id}))

@login_required
def ver_publicaciones(request, template_name):
    """
    Muestra las publicaciones, imágenes y comentarios en una página específica.

    Esta función recupera todas las imágenes, publicaciones y comentarios de la base de datos.
    Luego, formatea la fecha actual y calcula la diferencia en días para cada comentario.
    Además, obtiene el número de comentarios por publicación y formatea la fecha de publicación de la publicación.

    Parámetros:
    - request: HttpRequest
        La solicitud HTTP enviada al servidor.
    - template_name: str
        El nombre del template utilizado para renderizar la página.

    Retorna:
    - HttpResponse
        Una respuesta HTTP que renderiza la página con las imágenes, publicaciones y comentarios.
    """
    imagenes = Imagen.objects.all()
    publicaciones = Publicacion.objects.all()
    comentarios = Comentario.objects.all()  

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


@login_required
def ver_perfil(request, username):
    """
    Muestra el perfil de un usuario específico.

    Esta función recupera el perfil de un usuario específico y muestra sus publicaciones, comentarios e imágenes asociadas.
    Además, formatea la fecha de publicación de las publicaciones y calcula la diferencia en días para cada comentario.

    Parámetros:
    - request: HttpRequest
        La solicitud HTTP enviada al servidor.
    - username: str
        El nombre de usuario del perfil que se va a ver.

    Retorna:
    - HttpResponse
        Una respuesta HTTP que renderiza la página del perfil del usuario especificado.
    """
    user = User.objects.get(username=username)
    foto_de_perfil = user.perfil.profile_pic
    ahora = datetime.now().date()
    # Obtener el usuario correspondiente al nombre de usuario
    
    # Filtrar las publicaciones por el usuario
    publicaciones = Publicacion.objects.filter(user_id=user.id)
    comentarios = Comentario.objects.all()
    imagenes = Imagen.objects.all()
    for publicacion in publicaciones:
        publicacion.numero_de_comentarios = publicacion.comentarios.count()
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

@login_required
def agregar_comentario(request, id):
    """
    Agrega un comentario a una publicación específica.

    Esta función maneja la solicitud de agregar un comentario a una publicación específica.
    Si la solicitud es POST y el formulario de comentario es válido, guarda el comentario en la base de datos
    y redirige al usuario de vuelta a la página de perfil o al feed, dependiendo de su ubicación anterior.

    Parámetros:
    - request: HttpRequest
        La solicitud HTTP enviada al servidor.
    - id: int
        El identificador único de la publicación a la que se va a agregar el comentario.

    Retorna:
    - HttpResponseRedirect
        Redirección a la página de perfil del usuario que publicó la publicación o al feed, dependiendo de la ubicación anterior.
    """
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
                # Si estaba en la página de perfil, redirigir de vuelta a esa página
                return redirect(reverse('ver_perfil', kwargs={'username': usuario_publicacion.username}))
            elif 'listado_publicaciones' in request.META.get('HTTP_REFERER', ''):
                # Si estaba en la página de listado de publicaciones, redirigir de vuelta a esa página
                return redirect("listado_publicaciones")
        
    # De lo contrario, redirigir a la página de feed
    return redirect('feed')
    
    
                        
@login_required
def editar_perfil(request):
    """
    Permite al usuario editar su perfil.

    Esta función maneja la solicitud de editar el perfil de un usuario.
    Si la solicitud es POST y ambos formularios (usuario y perfil) son válidos,
    guarda los cambios en la base de datos y redirige al usuario a su página de perfil.

    Parámetros:
    - request: HttpRequest
        La solicitud HTTP enviada al servidor.

    Retorna:
    - HttpResponse
        Una respuesta HTTP que renderiza la página de edición de perfil del usuario.
    """
    perfil_usuario = Perfil.objects.get(username=request.user)
    usuario = User.objects.get(username=request.user)
    if request.method == 'POST':
        form_user = EditarPerfilForm(request.POST, instance=usuario)
        form_perfil = PerfilForm(request.POST, request.FILES, instance=perfil_usuario)
       
        if form_user.is_valid():
            if form_perfil.is_valid():
                usuario = form_user.save(commit=False)
                usuario.save()

                # Verificar si se ha subido una nueva imagen de perfil
                if 'profile_pic' in request.FILES:
                    nueva_imagen = request.FILES['profile_pic']
                    perfil_usuario.profile_pic = nueva_imagen
                    perfil_usuario.save()
                else:
                    # Si no se ha subido una nueva imagen de perfil, simplemente guardar el formulario
                    form_perfil.save()

                # Redirigir a la página de perfil del usuario después de editar el perfil
                return redirect(reverse('ver_perfil', kwargs={'username': request.POST['username']}))
    else:
        form_user = EditarPerfilForm(instance=usuario)
        form_perfil = PerfilForm(instance=perfil_usuario)

    return render(request, "perfil/editar_perfil.html", {"form_user": form_user, "form_perfil": form_perfil})



@login_required
def recursos(request):
    """
    Muestra los recursos disponibles en la plataforma.

    Esta función recupera todos los recursos y iframes de la base de datos.
    Luego, formatea la fecha de publicación de los recursos y modifica los iframes para extraer solo el contenido del atributo src.

    Parámetros:
    - request: HttpRequest
        La solicitud HTTP enviada al servidor.

    Retorna:
    - HttpResponse
        Una respuesta HTTP que renderiza la página de recursos con la lista de recursos e iframes disponibles.
    """
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
            # Modifica cada iframe para extraer solo el contenido del atributo src
            for iframe in iframes:
                codigo = iframe.codigo_iframe
                
                # Utiliza una expresión regular para encontrar el valor de src en el código del iframe
                match = re.search(r'src="([^"]+)"', codigo)
                
                # Verifica si se encontró un match y obtiene el contenido de src en minúsculas
                if match:
                    src_value = match.group(1)
                    iframe.codigo_iframe = src_value  # Actualiza el código del iframe
               
    
    return render(request, "perfil/recursos.html", {"recursos": recursos, "iframes": iframes, "src_value": src_value})

@login_required
def agregar_recurso(request):
    """
    Agrega un nuevo recurso a la plataforma.

    Esta función maneja la solicitud de agregar un nuevo recurso a la plataforma.
    Si la solicitud es POST y el formulario de recurso es válido, guarda el recurso en la base de datos
    y redirige al usuario de vuelta a la página de recursos.

    Parámetros:
    - request: HttpRequest
        La solicitud HTTP enviada al servidor.

    Retorna:
    - HttpResponseRedirect
        Redirección a la página de recursos después de agregar un nuevo recurso.
    """
    if request.method == 'POST':
        form_recurso = RecursosForm(request.POST, request.FILES)
        if form_recurso.is_valid():
            form_recurso.save()
            return redirect('recursos') 
    else:
        form_recurso = RecursosForm()
    
    recursos = Recursos.objects.all()
    for recurso in recursos:
        recurso.fecha_publicacion_recurso = recurso.fecha_publicacion_recurso.strftime("%d de %B de %Y")
    
    return render(request, 'perfil/agregar_recurso.html', {"form_recurso": form_recurso, "recursos": recursos})

@login_required
def agregar_recurso_externo(request):
    """
    Agrega un nuevo recurso externo a la plataforma.

    Esta función maneja la solicitud de agregar un nuevo recurso externo a la plataforma.
    Si la solicitud es POST y el formulario de recurso externo es válido, guarda el recurso externo en la base de datos
    y redirige al usuario de vuelta a la página de recursos.

    Parámetros:
    - request: HttpRequest
        La solicitud HTTP enviada al servidor.

    Retorna:
    - HttpResponseRedirect
        Redirección a la página de recursos después de agregar un nuevo recurso externo.
    """
    recursos_externos = Iframe.objects.all()
    if request.method == 'POST':
        form_recurso_externo = IframeForm(request.POST)
        if form_recurso_externo.is_valid():
            form_recurso_externo.save()
            return redirect('recursos')  
    else:
        form_recurso_externo = IframeForm()
    
    return render(request, 'perfil/agregar_recurso_externo.html', {"form_recurso_externo": form_recurso_externo, "recursos_externos": recursos_externos})

@login_required
def eliminar_recurso_externo(request,id):
    """
    Elimina un recurso externo de la plataforma.

    Esta función maneja la solicitud de eliminar un recurso externo de la plataforma.
    Elimina el recurso externo de la base de datos y redirige al usuario de vuelta a la página de recursos.

    Parámetros:
    - request: HttpRequest
        La solicitud HTTP enviada al servidor.
    - id: int
        El identificador único del recurso externo que se va a eliminar.

    Retorna:
    - HttpResponseRedirect
        Redirección a la página de recursos después de eliminar un recurso externo.
    """
    recurso_externo = Iframe.objects.get(id = id)
    recurso_externo.delete()
    return redirect("recursos")

@login_required
def eliminar_recurso(request, id):
    """
    Elimina un recurso de la plataforma.

    Esta función maneja la solicitud de eliminar un recurso de la plataforma.
    Elimina el recurso de la base de datos y su archivo asociado del sistema de archivos,
    luego redirige al usuario de vuelta a la página de recursos.

    Parámetros:
    - request: HttpRequest
        La solicitud HTTP enviada al servidor.
    - id: int
        El identificador único del recurso que se va a eliminar.

    Retorna:
    - HttpResponseRedirect
        Redirección a la página de recursos después de eliminar un recurso.
    """
    recurso = Recursos.objects.get(id=id)
    
    # Obtener la ruta del archivo asociado al recurso
    archivo_ruta = recurso.archivo_recurso.path
    
    # Eliminar el recurso de la base de datos
    recurso.delete()
    
    # Eliminar el archivo del sistema de archivos
    if os.path.exists(archivo_ruta):
        os.remove(archivo_ruta)
    
    return redirect("recursos")

@login_required
def editar_recurso(request,id):
    """
    Edita un recurso de la plataforma.

    Esta función maneja la solicitud de editar un recurso de la plataforma.
    Si la solicitud es POST y el formulario de recurso es válido, guarda los cambios en la base de datos
    y redirige al usuario de vuelta a la página de recursos.

    Parámetros:
    - request: HttpRequest
        La solicitud HTTP enviada al servidor.
    - id: int
        El identificador único del recurso que se va a editar.

    Retorna:
    - HttpResponseRedirect
        Redirección a la página de recursos después de editar un recurso.
    """
    recurso = Recursos.objects.get(id = id)
    form_recurso = RecursosForm(request.POST or None, request.FILES or None, instance = recurso)
    if form_recurso.is_valid() and request.POST:
        form_recurso.save()
        return redirect("agregar_recurso")
    return render(request, "perfil/editar_recurso.html", {"form_recurso": form_recurso, "recurso": recurso})

@login_required
def editar_recurso_externo(request,id):
    """
    Edita un recurso externo de la plataforma.

    Esta función maneja la solicitud de editar un recurso externo de la plataforma.
    Si la solicitud es POST y el formulario de recurso externo es válido, guarda los cambios en la base de datos
    y redirige al usuario de vuelta a la página de recursos.

    Parámetros:
    - request: HttpRequest
        La solicitud HTTP enviada al servidor.
    - id: int
        El identificador único del recurso externo que se va a editar.

    Retorna:
    - HttpResponseRedirect
        Redirección a la página de recursos después de editar un recurso externo.
    """
    recurso_externo = Iframe.objects.get(id = id)
    form_recurso_externo = IframeForm(request.POST or None, instance = recurso_externo)
    if form_recurso_externo.is_valid() and request.POST:
        form_recurso_externo.save()
        return redirect("recursos")
    return render(request, "perfil/editar_recurso_externo.html", {"form_recurso_externo": form_recurso_externo, "recurso_externo": recurso_externo})

@login_required
def calendario(request):
    """
    Muestra el calendario de eventos del usuario.

    Esta función recupera el calendario de eventos del usuario y lo muestra en una página.

    Parámetros:
    - request: HttpRequest
        La solicitud HTTP enviada al servidor.

    Retorna:
    - HttpResponse
        Una respuesta HTTP que renderiza la página del calendario de eventos del usuario.
    """
    user = request.user
    return render(request, "perfil/calendario.html", {"user": user})