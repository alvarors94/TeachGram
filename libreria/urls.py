from django.urls import path, include
from . import views # el . indica que de esta misma carpeta, importe views.py
from django.conf import settings # para usar estos archivos en la carpeta settings
from django.contrib.staticfiles.urls import static # para usar estos archivos en la carpeta static

urlpatterns = [
    path("", views.ver_publicaciones, {"template_name": "perfil/feed.html"}, name="feed"),
    path("listado_perfiles", views.listado_perfiles, {"template_name": "perfil/listado_perfiles.html"}, name="listado_perfiles"),
    path("clase", views.listado_perfiles, {"template_name": "perfil/clase.html"}, name="clase"),
    path("crear_publicacion", views.crear_publicacion, name="crear_publicacion"), 
    path("editar_publicacion/<int:id>", views.editar_publicacion, name="editar_publicacion"), 
    path("editar_comentario/<int:id>", views.editar_comentario, name="editar_comentario"), 
    path("editar_perfil", views.editar_perfil, name="editar_perfil"),
    path("cambiar_password", views.CambiarPassword.as_view(), name="cambiar_password"), 
    path("eliminar_publicacion/<int:id>", views.eliminar_publicacion, name="eliminar_publicacion"),
    path("eliminar_comentario/<int:id>", views.eliminar_comentario, name="eliminar_comentario"), 
    path("listado_publicaciones", views.ver_publicaciones, {"template_name": "perfil/listado_publicaciones.html"}, name="listado_publicaciones"),
    path("agregar_comentario/<int:id>", views.agregar_comentario, name="agregar_comentario"),  
    path("perfil/<str:username>", views.ver_perfil, name="ver_perfil"),
    path("agregar_recurso_externo", views.agregar_recurso_externo, name="agregar_recurso_externo"),
    path("recursos", views.recursos, name="recursos"),
    path("agregar_recurso", views.agregar_recurso, name="agregar_recurso"),
    path("eliminar_recurso/<int:id>", views.eliminar_recurso, name="eliminar_recurso"),
    path("eliminar_recurso_externo/<int:id>", views.eliminar_recurso_externo, name="eliminar_recurso_externo"),
    path("editar_recurso/<int:id>", views.editar_recurso, name="editar_recurso"),
    path("editar_recurso_externo/<int:id>", views.editar_recurso_externo, name="editar_recurso_externo"),
    path("eliminar_imagen/<int:id>", views.eliminar_imagen, name="eliminar_imagen"),
    path("crear_usuario", views.crear_usuario, name="crear_usuario"),
    path("eliminar_perfil/<int:id>", views.eliminar_perfil, name="eliminar_perfil"),
    path("bloquear_perfil/<int:id>", views.bloquear_perfil, name="bloquear_perfil"),
    path("hacer_superusuario/<int:id>", views.hacer_superusuario, name="hacer_superusuario"),
    path("calendario", views.calendario, name="calendario"),

    
   

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # así concatenamos el path de la carpeta media y la ruta de la carpeta static



#Add Django site authentication urls (for login, logout, password management)
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]