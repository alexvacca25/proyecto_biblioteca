# controllers/admin_controller.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash
from models.user import User
from models.book import Book
from models.loan import Loan
from extensions import db
from datetime import datetime

admin_bp = Blueprint('admin', __name__)

def is_admin():
    """Verificar si el usuario actual es administrador"""
    return session.get('user_id') and session.get('role') == True

@admin_bp.route('/admin_dashboard')
def admin_dashboard():
    if not is_admin():
        flash("Acceso denegado: Solo los administradores pueden acceder a esta sección.", "danger")
        return redirect(url_for('auth.login'))
    
    users = User.query.all()
    books = Book.query.all()
    loans = Loan.query.all()  # Obtener todos los préstamos
    return render_template('admin_dashboard.html', users=users, books=books, loans=loans)

# Rutas para gestionar usuarios (CRUD)
@admin_bp.route('/manage_users', methods=['GET', 'POST'])
def manage_users():
    if not is_admin():
        flash("Acceso denegado: Solo los administradores pueden acceder a esta sección.", "danger")
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        first_name=request.form['first_name']
        last_name=request.form['last_name']
        address=request.form['address']
        phone=request.form['phone']
        role = True if request.form.get('role') == 'admin' else False
        
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("El nombre de usuario ya existe.", "danger")
            return redirect(url_for('admin.manage_users'))
        
        new_user = User(username=username, password=generate_password_hash(password),first_name=first_name,last_name=last_name, address=address, phone=phone, role=role)
        db.session.add(new_user)
        db.session.commit()
        flash("Usuario creado exitosamente.", "success")
        return redirect(url_for('admin.manage_users'))
    
    users = User.query.all()
    return render_template('manage_users.html', users=users)

@admin_bp.route('/toggle_role/<int:user_id>', methods=['POST'])
def toggle_role(user_id):
    user = User.query.get(user_id)
    if user:
        user.role = not user.role  # Cambiar el rol del usuario
        db.session.commit()
        flash("Rol del usuario actualizado exitosamente.", "success")
    else:
        flash("Usuario no encontrado.", "danger")
    return redirect(url_for('admin.manage_users'))

@admin_bp.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    if not is_admin():
        flash("Acceso denegado: Solo los administradores pueden eliminar usuarios.", "danger")
        return redirect(url_for('auth.login'))
    
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        flash("Usuario eliminado exitosamente.", "success")
    else:
        flash("Usuario no encontrado.", "danger")
    
    return redirect(url_for('admin.manage_users'))

# Rutas para gestionar libros (CRUD)
@admin_bp.route('/manage_books', methods=['GET', 'POST'])
def manage_books():
    if not is_admin():
        flash("Acceso denegado: Solo los administradores pueden acceder a esta sección.", "danger")
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        anno_publica=request.form['anno_publica']
        serie=request.form['serie']
        
        # Verificar si el libro ya existe
        existing_book = Book.query.filter_by(title=title).first()
        if existing_book:
            flash("El libro ya existe.", "danger")
            return redirect(url_for('admin.manage_books'))
        
        new_book = Book(title=title, author=author, available=True,anno_publica=anno_publica,serie=serie)
        db.session.add(new_book)
        db.session.commit()
        flash("Libro creado exitosamente.", "success")
        return redirect(url_for('admin.manage_books'))

    books = Book.query.all()
    return render_template('manage_books.html', books=books)

@admin_bp.route('/delete_book/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    if not is_admin():
        flash("Acceso denegado: Solo los administradores pueden eliminar libros.", "danger")
        return redirect(url_for('auth.login'))
    
    book = Book.query.get(book_id)
    if book:
        db.session.delete(book)
        db.session.commit()
        flash("Libro eliminado exitosamente.", "success")
    else:
        flash("Libro no encontrado.", "danger")
    
    return redirect(url_for('admin.manage_books'))

# Rutas para gestionar préstamos
@admin_bp.route('/manage_loans', methods=['GET', 'POST'])
def manage_loans():
    if not is_admin():
        flash("Acceso denegado: Solo los administradores pueden acceder a esta sección.", "danger")
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        user_id = request.form['user_id']
        book_id = request.form['book_id']

        # Verificar si el usuario y el libro existen
        user = User.query.get(user_id)
        book = Book.query.get(book_id)

        if not user:
            flash("Usuario no encontrado.", "danger")
            return redirect(url_for('admin.manage_loans'))
        
        if not book or not book.available:
            flash("El libro no está disponible para préstamo.", "danger")
            return redirect(url_for('admin.manage_loans'))

        # Crear el préstamo
        new_loan = Loan(user_id=user_id, book_id=book_id)
        book.available = False  # Marcar el libro como no disponible
        db.session.add(new_loan)
        db.session.commit()

        flash("Préstamo creado exitosamente.", "success")
        return redirect(url_for('admin.manage_loans'))

    # Obtener la lista de usuarios y libros disponibles para el formulario de creación de préstamo
    users = User.query.all()
    books = Book.query.filter_by(available=True).all()
    loans = Loan.query.all()  # Obtener todos los préstamos para mostrarlos
    return render_template('manage_loans.html', users=users, books=books, loans=loans)

@admin_bp.route('/return/<int:loan_id>', methods=['POST'])
def return_book(loan_id):
    if not is_admin():
        flash("Acceso denegado: Solo los administradores pueden devolver libros.", "danger")
        return redirect(url_for('auth.login'))
    
    loan = Loan.query.get(loan_id)
    if loan:
        loan.is_returned = True
        loan.return_date = datetime.now()
        # Marcar el libro como disponible nuevamente
        book = loan.book
        book.available = True
        db.session.commit()
        flash("Préstamo marcado como devuelto", "success")
    else:
        flash("Préstamo no encontrado", "danger")
    return redirect(url_for('admin.manage_loans'))

@admin_bp.route('/edit_book/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    if not is_admin():
        flash("Acceso denegado: Solo los administradores pueden acceder a esta sección.", "danger")
        return redirect(url_for('auth.login'))
    
    book = Book.query.get(book_id)
    
    if request.method == 'POST':
        book.title = request.form['title']
        book.author = request.form['author']
        db.session.commit()
        flash("Libro actualizado exitosamente.", "success")
        return redirect(url_for('admin.manage_books'))
    
    return render_template('edit_book.html', book=book)