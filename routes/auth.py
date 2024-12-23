from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from db import get_connection

auth_bp = Blueprint('auth', __name__)

# Ruta para el registro
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        #hashed_password = generate_password_hash(password, method='sha256')
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        try:
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
                (username, email, hashed_password)
            )
            connection.commit()
            flash('Usuario registrado con éxito', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            flash(f'Error al registrar usuario: {e}', 'danger')
        finally:
            if connection:
                cursor.close()
                connection.close()

    return render_template('register.html')


# Ruta para el inicio de sesión
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()

            if user and check_password_hash(user[3], password):  # user[3] es la columna password_hash
                session['user_id'] = user[0]
                session['username'] = user[1]
                flash('Inicio de sesión exitoso', 'success')
                return redirect(url_for('index'))
            else:
                flash('Credenciales incorrectas', 'danger')
        except Exception as e:
            flash(f'Error al iniciar sesión: {e}', 'danger')
        finally:
            if connection:
                cursor.close()
                connection.close()

    return render_template('login.html')


# Ruta para cerrar sesión
@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Has cerrado sesión', 'success')
    return redirect(url_for('auth.login'))
