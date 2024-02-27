from django.urls import path, include
from . import views # el . indica que de esta misma carpeta, importe views.py
from django.conf import settings # para usar estos archivos en la carpeta settings
from django.contrib.staticfiles.urls import static # para usar estos archivos en la carpeta static




urlpatterns = [
    path("", views.inicio, name="inicio"), # "" indica la ruta 127.0.0.1:8000
    path("perfil", views.perfil, name="perfil"),
    path("crear_publicacion", views.crear_publicacion, name="crear_publicacion"), 
    path("editar_publicacion/<int:id>", views.editar_publicacion, name="editar_publicacion"), 
    path("editar_comentario/<int:id>", views.editar_comentario, name="editar_comentario"), 
    path("editar_perfil/<str:username>", views.editar_perfil, name="editar_perfil"),
    path("cambiar_password", views.CambiarPassword.as_view(), name="cambiar_password"), 
    path("eliminar_publicacion/<int:id>", views.eliminar_publicacion, name="eliminar_publicacion"),
    path("eliminar_comentario/<int:id>", views.eliminar_comentario, name="eliminar_comentario"), 
    path("listado_publicaciones", views.ver_publicaciones, {"template_name": "perfil/listado_publicaciones.html"}, name="listado_publicaciones"),
    path("feed", views.ver_publicaciones, {"template_name": "perfil/feed.html"}, name="feed"),
    path("ver_comentarios/<int:id>", views.ver_publicaciones, {"template_name": "perfil/feed.html"}, name="ver_comentarios"),  # Utiliza la misma vista para ver comentarios en el feed
    path("feed/ver_comentarios/<int:id>", views.ver_comentarios, name="feed_ver_comentarios"),  # Nueva ruta para ver comentarios en el feed
    path("agregar_comentario/<int:id>", views.agregar_comentario, name="agregar_comentario"),  
    path("perfil/<str:username>", views.ver_perfil, name="ver_perfil"),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # así concatenamos el path de la carpeta media y la ruta de la carpeta static



#Add Django site authentication urls (for login, logout, password management)
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]