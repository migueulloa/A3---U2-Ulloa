# --- INICIO DE MODIFICACIONES ---
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_required
# --- FIN DE MODIFICACIONES ---
from werkzeug.security import generate_password_hash, check_password_hash
import controllers 
from database import db 
# --- INICIO DE MODIFICACIONES ---
from models import Juegos, User # Importa User
from auth import auth as auth_blueprint # Importa el blueprint
# --- FIN DE MODIFICACIONES ---

app = Flask(__name__)

# --- INICIO DE MODIFICACIONES ---
# Paso 2: Añadir SECRET_KEY
# ¡Cambia esto por una cadena aleatoria y segura!
app.config['SECRET_KEY'] = 'esta-es-una-llave-muy-secreta'
# --- FIN DE MODIFICACIONES ---

login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'
login_manager.session_protection = 'strong'

# Configuración de Flask-SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:hola123@localhost/juegos'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# --- INICIO DE MODIFICACIONES ---
# Paso 4: Implementar la función callback
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Paso 6: Registrar el blueprint
app.register_blueprint(auth_blueprint, url_prefix='/auth')
# --- FIN DE MODIFICACIONES ---


@app.route("/agregar_juego")
@login_required # Paso 7: Proteger ruta
def formulario_agregar_juego():
    return render_template("agregar_juego.html")

@app.route("/guardar_juego", methods=["POST"])
@login_required # Paso 7: Proteger ruta
def guardar_juego():
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    precio = request.form["precio"]
    controllers.insertar_juego(nombre, descripcion, precio)
    # --- INICIO DE MODIFICACIONES ---
    flash("Juego guardado correctamente") # Añadir feedback
    return redirect(url_for('juegos')) # Usar url_for
    # --- FIN DE MODIFICACIONES ---

@app.route("/")
@app.route("/juegos")
@login_required # Paso 7: Proteger ruta
def juegos():
    juegos = controllers.obtener_juegos()
    return render_template("juegos.html", juegos=juegos)

@app.route("/eliminar_juego", methods=["POST"])
@login_required # Paso 7: Proteger ruta
def eliminar_juego():
    controllers.eliminar_juego(request.form["id"])
    # --- INICIO DE MODIFICACIONES ---
    flash("Juego eliminado correctamente")
    return redirect(url_for('juegos'))
    # --- FIN DE MODIFICACIONES ---

@app.route("/formulario_editar_juego/<int:id>")
@login_required # Paso 7: Proteger ruta
def editar_juego(id):
    juego = controllers.obtener_juego_por_id(id)
    return render_template("editar_juego.html", juego=juego)

@app.route("/actualizar_juego", methods=["POST"])
@login_required # Paso 7: Proteger ruta
def actualizar_juego():
    id = request.form["id"]
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    precio = request.form["precio"]
    controllers.actualizar_juego(nombre, descripcion, precio, id)
    # --- INICIO de MODIFICACIONES ---
    flash("Juego actualizado correctamente")
    return redirect(url_for('juegos'))
    # --- FIN DE MODIFICACIONES ---

if __name__ == "__main__":
    # --- INICIO DE MODIFICACIONES ---
    # Añadimos esto para que cree las tablas (incluida la de User)
    # la primera vez que se ejecute la app.
    with app.app_context():
        db.create_all()
    # --- FIN DE MODIFICACIONES ---
    app.run(host="127.0.0.1", port=8000, debug=True)