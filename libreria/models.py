from django.db import models
from django.conf import settings


class Usuario(models.Model):
    id_usuario=models.AutoField(primary_key=True) #Autoincremental
    nombre_usuario = models.CharField(max_length=200, unique=True, verbose_name="Nombre de usuario")
    nombre_completo = models.CharField(max_length=200, verbose_name="Nombre completo")
    password = models.CharField(max_length=200, verbose_name="Contraseña")
    foto_perfil = models.ImageField(upload_to="media/profile_pics", default='media/avatar.png', verbose_name="Foto de perfil")
    esta_bloqueado = models.BooleanField(default=False)
    def __str__(self):
        return f"Usuario {self.nombre_usuario}, Nombre completo: {self.nombre_completo}"

    def delete(self): # Con esta función, cuando se borra el usuario también se boora la foto de perfil del almacenamiento
        super().delete()

class Publicacion(models.Model):
    id_publicacion=models.AutoField(primary_key=True) #Autoincremental
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='publicaciones')
    foto_publicacion = models.ImageField(upload_to="static/publicaciones", verbose_name="Imagen")
    descripcion = models.CharField(max_length=200, null=False, verbose_name="Descripción")
    fecha_publicacion = models.DateField(auto_now_add=True, verbose_name="Fecha de publicación")

    def __str__(self):
        return f"Usuario {self.usuario}: {self.descripcion}, Fecha: {self.fecha_publicacion}"


class Comentario(models.Model):
    id_comentario=models.AutoField(primary_key=True) #Autoincremental
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    publicacion = models.ForeignKey(Publicacion, on_delete=models.CASCADE, related_name='comentarios')
    comentario = models.CharField(max_length=400, verbose_name="Comentario")
    fecha_publicacion_comentario = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario}'s comment ({self.comentario}) Fecha: {self.fecha_publicacion_comentario}"

