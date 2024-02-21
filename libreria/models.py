from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin



class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('El superusuario debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('El superusuario debe tener is_superuser=True.')

        return self.create_user(username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=200, unique=True, verbose_name="Nombre de usuario")
    full_name = models.CharField(max_length=200, verbose_name="Nombre completo", blank=True, null=True)
    profile_pic = models.ImageField(
        upload_to="media/profile_pics",
        default='media/avatar.png',
        verbose_name="Foto de perfil",
        blank=True,
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    groups = models.ManyToManyField('Group', related_name='users')
    user_permissions = models.ManyToManyField('Permission', related_name='user_permissions_users')

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

class Publicacion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')
    foto_publicacion = models.ImageField(upload_to="publicaciones", verbose_name="Imagen")
    descripcion = models.CharField(max_length=200, verbose_name="Descripción")
    fecha_publicacion = models.DateField(auto_now_add=True, verbose_name="Fecha de publicación")


class Comentario(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    publicacion = models.ForeignKey(Publicacion, on_delete=models.CASCADE, related_name='comentarios')
    comentario = models.CharField(max_length=400, verbose_name="Comentario")
    fecha_publicacion_comentario = models.DateField(auto_now_add=True)


class Group(models.Model):
    name = models.CharField(max_length=150, unique=True)
    

class Permission(models.Model):
    name = models.CharField(max_length=255)
    codename = models.CharField(max_length=100)
