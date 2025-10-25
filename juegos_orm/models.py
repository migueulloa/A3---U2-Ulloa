from database import db
# --- INICIO DE MODIFICACIONES ---
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
# --- FIN DE MODIFICACIONES ---

class Juegos(db.Model):
    __tablename__ = 'juegos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.String(255), nullable=False)
    precio = db.Column(db.Numeric(9,2), nullable=False)

# --- INICIO DE MODIFICACIONES ---
# Asegúrate que la clase herede de UserMixin
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(256))

    @property
    def password(self):
        raise AttributeError('password is write-only')
    
    # Método setter para hashear la contraseña
    @password.setter
    def password(self, pwd):
        self.password_hash = generate_password_hash(pwd)

    # Método para verificar la contraseña
    def verify_password(self, pwd):
        return check_password_hash(self.password_hash, pwd)
# --- FIN DE MODIFICACIONES ---