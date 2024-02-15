from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# El "engine" permite a SQLAlchemy comunicarse con la base de datos de un dialecto concreto
# La forma de crear el engine depende de cada dialecto, aunque su estructura es la siguiente:
# engine = create_engine(dialecto, nombre_bbdd)
# https://docs.sqlalchemy.org/en/14/core/engines.html
# Para SQLite es la siguiente:
engine = create_engine(
    "sqlite:///database/teachgram.db",  # database es el nombre de la carpeta donde va a ir esta nueva base de datos
    connect_args={"check_same_thread": False})
# Esta última línea le dice al programa que no hace falta hacerlo todo en el mismo hilo de ejecución

# También dependiendo del dialecto, la forma de introducir usuarios y contraseña cambia
# Crear el engine, no conecta inmediatamente con la base de datos

# Ahora hay que crear un objeto (sesion) que se encargue de las transacciones dentro de la base de datos
Session = sessionmaker(bind=engine)  # Se pone S mayúscula porque es una clase
session = Session()  # Instanciamos la clase

# Esta instrucción lo que hace es buscar en models.py las clases para transformarlas en tablas
Base = declarative_base()
