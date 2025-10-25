# auth.py (Archivo nuevo)

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from flask_login import login_user, logout_user, login_required
from models import User
from database import db
from werkzeug.security import check_password_hash, generate_password_hash

# Paso 5: Crear el blueprint
auth = Blueprint('auth', __name__)

# Paso 5: Definir el formulario de Login
class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember_me = BooleanField('Recordarme')
    submit = SubmitField('Ingresar')

# Formulario de Registro (Implícito en el paso 6)
class RegisterForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Registrar')

# Paso 6: Implementar las rutas
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            # Redirige a la página de juegos después del login
            return redirect(request.args.get('next') or url_for('juegos'))
        flash('Usuario o contraseña inválidos.')
    return render_template('login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión.')
    return redirect(url_for('auth.login'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # Verifica si el usuario ya existe
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user is None:
            new_user = User(username=form.username.data)
            new_user.password = form.password.data # El setter se encarga del hash
            db.session.add(new_user)
            db.session.commit()
            flash('Usuario registrado exitosamente. Ahora puedes ingresar.')
            return redirect(url_for('auth.login'))
        flash('Ese nombre de usuario ya existe.')
    return render_template('register.html', form=form)