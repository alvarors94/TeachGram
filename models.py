# La clase necesita heredar de la clase Base para crear las tablas
# Como está en otro archivo, necesitamos importarlo.
# Para ello importamos el nombre del archivo donde se encuentre la clase en este caso db.py
import db
from sqlalchemy import Column, Integer, String, Date, func, ForeignKey, relationship
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
 
# Con esto quiere decir que cuando se instancie un objeto, se cree en la base de datos
class Usuario(db.Base):
    __tablename__ = "usuario"
    __table_args__ = {"sqlite_autoincrement": True}  # Forzamos que en la tabla haya un valor que sea autoincremental
    id_usuario = Column(Integer, primary_key=True)  # Creamos la columna del id_que tendrá la primary key
    nombre_usuario = Column(String(200), nullable=False)  # Creamos las columnas de los campos definidos
    nombre_completo = Column(String(200), nullable=False)
    password = Column(String(200), nullable=False)
    profile_pic = models.ImageField(
        upload_to="static\profile_pics",
        default='avatar.png')
    publicaciones = relationship("Publicacion", back_populates="usuario")  # Definimos la relación inversa

    def __init__(self, id_usuario, nombre_usuario, nombre_completo, password, publicaciones):
        self.id_usuario = id_usuario
        self.nombre_usuario = nombre_usuario
        self.nombre_completo = nombre_completo
        self.password = password
        self.publicaciones = publicaciones
        
        print("Usuario creado con éxito")

    def __str__(self):
        return f"Usuario {self.id_usuario}, Nombre: {self.nombre_usuario}, Nombre completo: {self.nombre_completo}, Password: {self.password}, Publicaciones: {self.publicaciones}"
    
    
class Publicacion(db.Base):
    __tablename__ = "publicacion"
    __table_args__ = {"sqlite_autoincrement": True}
    id_publicacion = Column(Integer, primary_key=True)
    id_usuario = Column(Integer, ForeignKey('usuario.id_usuario'))  # Definimos la clave externa
    usuario = relationship("Usuario", back_populates="publicaciones")  # Definimos la relación con la clase Usuario
    descripcion = Column(String(200))
    fecha_publicacion = Column(Date, server_default=func.now())

    def __init__(self, id_publicacion, id_usuario, descripcion, comentarios, fecha_publicacion):
        self.id_publicacion = id_publicacion
        self.id_usuario = id_usuario
        self.descripcion = descripcion
        self.fecha_publicacion = fecha_publicacion
        print("Publicación creada con éxito")

    def __str__(self):
        return f"Publicación {self.id_publicacion}, Usuario {self.id_usuario}: {self.descripcion}, Comentarios: {self.comentarios}, ({self.fecha_publicacion}) "
    
class Comentarios(db.Base):
    __tablename__ = "comentarios"
    __table_args__ = {"sqlite_autoincrement": True}
    id_comentario = Column(Integer, primary_key=True)
    id_publicacion = Column(Integer, ForeignKey('publicacion.id_publicacion'))
    id_usuario = Column(Integer, ForeignKey('usuario.id_usuario'))  # Definimos la clave externa
    comentario = Column(String(200))
    fecha_publicacion_comentario = Column(Date, server_default=func.now())
    
    def __init__(self, id_comentario, id_publicacion, id_usuario, comentario, fecha_publicacion_comentario):
        self.id_comentario = id_comentario
        self.id_publicacion = id_publicacion
        self.id_usuario = id_usuario
        self.comentario = comentario
        self.fecha_publicacion_comentario = fecha_publicacion_comentario
        print("Comentario creado con éxito")
    
    def __str__(self):
        return f'{self.id_usuario}\'s comment ({self.comentario})'