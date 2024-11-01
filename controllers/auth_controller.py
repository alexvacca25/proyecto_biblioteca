# controllers/auth_controller.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash, generate_password_hash
from extensions import db

auth_bp = Blueprint('auth', __name__)
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    from models.user import User  # Importación local para evitar ciclo
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role  # Guardar el rol en la sesión

            # Redirigir a la vista correspondiente según el rol
            if user.role:  # Si es administrador
                return redirect(url_for('admin.admin_dashboard'))
            else:  # Si es un usuario normal
                return redirect(url_for('user.dashboard'))
        else:
            flash("Nombre de usuario o contraseña incorrectos", "danger")
            return render_template('login.html', message="Nombre de usuario o contraseña incorrectos")
    
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    # Limpiar la sesión
    session.clear()
    flash("Sesión cerrada exitosamente", "success")
    return redirect(url_for('auth.login'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    from models.user import User  # Importación local para evitar ciclos de importación
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Verificar si el nombre de usuario ya está en uso
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("El nombre de usuario ya está en uso", "danger")
            return render_template('register.html', message="El nombre de usuario ya está en uso")
        
        # Crear nuevo usuario con contraseña encriptada
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash("Usuario registrado exitosamente", "success")
        return redirect(url_for('auth.login'))
    
    return render_template('register.html')
