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

app.config['SECRET_KEY'] = 'esta-es-una-llave-muy-secreta'

login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'
login_manager.session_protection = 'strong'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:hola123@localhost/juegos'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.register_blueprint(auth_blueprint, url_prefix='/auth')

@app.route("/agregar_juego")
@login_required 
def formulario_agregar_juego():
    return render_template("agregar_juego.html")

@app.route("/guardar_juego", methods=["POST"])
@login_required 
def guardar_juego():
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    precio = request.form["precio"]
    controllers.insertar_juego(nombre, descripcion, precio)
    flash("Juego guardado correctamente")
    return redirect(url_for('juegos')) 

@app.route("/")
@app.route("/juegos")
@login_required 
def juegos():
    juegos = controllers.obtener_juegos()
    return render_template("juegos.html", juegos=juegos)

@app.route("/eliminar_juego", methods=["POST"])
@login_required 
def eliminar_juego():
    controllers.eliminar_juego(request.form["id"])
    flash("Juego eliminado correctamente")
    return redirect(url_for('juegos'))

@app.route("/formulario_editar_juego/<int:id>")
@login_required 
def editar_juego(id):
    juego = controllers.obtener_juego_por_id(id)
    return render_template("editar_juego.html", juego=juego)

@app.route("/actualizar_juego", methods=["POST"])
@login_required 
def actualizar_juego():
    id = request.form["id"]
    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    precio = request.form["precio"]
    controllers.actualizar_juego(nombre, descripcion, precio, id)
    flash("Juego actualizado correctamente")
    return redirect(url_for('juegos'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="127.0.0.1", port=8000, debug=True)