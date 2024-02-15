from flask import Flask, render_template, redirect, url_for, request
import db
from models import Tarea
from datetime import datetime
app = Flask(__name__)


@app.route("/")  # Definimos el "endpoint" para la página de inicio
def home():  # No hace falta llamar a la función para ejecutarla
    todas_publiaciones = db.session.query(Tarea).all()
    return render_template("index.html", lista_publicaciones = todas_publiaciones)

@app.route("/guardar", methods=["POST"])# Creamos el "endpoint" de guardar
def guardar():
    contenido_tarea = request.form["contenido-tarea"] #Almacenamos los nuevos datos en variables
    fecha_limite_str = request.form["trip-start"]
    categoria_seleccionada = request.form["select-category"]
    fecha_limite = datetime.strptime(fecha_limite_str, "%Y-%m-%d").date()
    tarea = Tarea(contenido_tarea, categoria_seleccionada, False, fecha_limite) #Creamos una nueva tarea con estos datos
    db.session.add(tarea)
    db.session.commit()

    return home()

@app.route("/eliminar_tarea/<id>") # Creamos el "endpoint" de eliminar
def eliminar_tarea(id): # Creamos la función de eliminar tarea
    tarea = db.session.query(Tarea).filter_by(id_tarea = id)
    tarea.delete()
    db.session.commit() # Guardamos los cambios
    return home() #Redireccionamos de nuevo a la página de inicio


@app.route("/editar_tarea/<id>", methods=["GET", "POST"]) # Creamos el "endpoint" de editar
def editar_tarea(id):
    tarea_existente = db.session.query(Tarea).filter_by(id_tarea=id).first() #Buscamos la tarea por el id dado

    if request.method == "POST":
        if "contenido-tarea" in request.form:
            nuevo_contenido = request.form["contenido-tarea"] #Almacenamos los nuevos datos en variables
            nueva_categoria = request.form["select-category"]
            nueva_fecha_str = request.form["trip-start"]
            nueva_fecha = datetime.strptime(nueva_fecha_str, "%Y-%m-%d").date()

            tarea_existente.contenido = nuevo_contenido #ACtualizamos el contenido exitente por el nuevo
            tarea_existente.categoria = nueva_categoria
            tarea_existente.fecha_limite = nueva_fecha
            db.session.commit() #Guardamos los cambios en la base de datos
            return redirect(url_for('home'))  # Redirige a la página de inicio

    return render_template("editar.html", tarea=tarea_existente)

@app.route("/tarea_hecha/<id>") # Creamos el "endpoint" de tarea hecha
def tarea_hecha(id):
    tarea = db.session.query(Tarea).filter_by(id_tarea = id).first() # Al poner first, tarea pasa de ser de tipo Query a Tarea
    tarea.hecha = not(tarea.hecha) # Se pone así para poder marcarla como hecha y cambiar de nuevo su estado a no hecha
    db.session.commit() # Guardamos los cambios
    return home() #Redireccionamos de nuevo a la página de inicio

if __name__ == '__main__':
    
    # Con estas cuatro líneas, si escribimos "python main.py" en el terminal se levanta la aplicación
    # 127.0.0.1:5000 = localhost:5000

    # Los HTML hay que meterlos en una carpeta llamada "templates"
    # La primera página se tiene que llamar index.html

    # Los CSS se meten en una carpeta llamada "static" y se llamará main.css
    # Reseteamos la base de datos si existe (sólo para pruebas)
    # db.Base.metadata.drop_all(bind=db.engine, checkfirst=True)

    # Ahora indicamos a SQLAlchemy que cree, si no existe, la tabla de todos los modelos que encuentre en model.py
    # Esto crea la estructura de la base de datos, no introduce los datos
    db.Base.metadata.create_all(db.engine)

    app.run(debug=True) # ESta línea tiene que ser lo último