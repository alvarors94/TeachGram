from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Perfil(models.Model):
    username = models.OneToOneField(User,max_length=200, on_delete=models.CASCADE,unique=True, verbose_name="Nombre de usuario")
    profile_pic = models.ImageField(
        upload_to="media/profile_pics",
        default='media/avatar.png',
        verbose_name="Foto de perfil",
        blank=True,
    )
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return f'Perfil de {self.username}'

class Publicacion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='publicaciones')
    descripcion = models.CharField(max_length=200, verbose_name="Descripción")
    fecha_publicacion = models.DateField(auto_now_add=True, verbose_name="Fecha de publicación")

    class Meta:
        ordering = ['-id']
        
    def __str__(self):
        return f'{self.user.username}: {self.descripcion}'

class Imagen(models.Model):
    publicacion = models.ForeignKey(Publicacion, on_delete=models.CASCADE, related_name='imagenes')
    imagen = models.ImageField(upload_to="publicaciones", verbose_name="Imagen", blank=True, null=True)

    def __str__(self):
        return f'Imagen de la publicación: {self.publicacion.id}'
    
class Comentario(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comentario')
    publicacion = models.ForeignKey(Publicacion, on_delete=models.CASCADE,related_name='comentarios')
    comentario = models.CharField(max_length=400, verbose_name="Comentario")
    fecha_publicacion_comentario = models.DateField(auto_now_add=True)
    
    class Meta:
        ordering = ['-id']
    
class Recursos(models.Model):
    nombre = models.CharField(max_length=200, verbose_name="Nombre", default="Recursos")
    archivo_recurso = models.FileField(upload_to="media/recursos", verbose_name="Archivo")
    descripcion = models.CharField(max_length=400, verbose_name="Descripción")
    fecha_publicacion_recurso = models.DateField(auto_now_add=True, verbose_name="Fecha de publicación")

    class Meta:
        ordering = ['-id']
