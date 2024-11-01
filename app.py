# app.py
from flask import Flask, render_template
from extensions import db
from werkzeug.security import generate_password_hash

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SECRET_KEY'] = 'supersecretkey'
    
    db.init_app(app)

    # Registrar los blueprints de los diferentes módulos
    from controllers.auth_controller import auth_bp
    from controllers.admin_controller import admin_bp
    from controllers.user_controller import user_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(user_bp, url_prefix='/user')

    # Crear el contexto de aplicación para la base de datos y el usuario administrador por defecto
    with app.app_context():
        # Crear tablas si no existen
        db.create_all()

        # Crear usuario administrador por defecto si no existe
        from models.user import User
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            admin_user = User(
                username='admin',
                password=generate_password_hash('admin123'),  # Cambia la contraseña por una segura
                role=True  # Este usuario es un administrador
            )
            db.session.add(admin_user)
            db.session.commit()
            print("Usuario administrador creado con nombre de usuario 'admin' y contraseña 'admin123'.")

                # Ruta principal
    @app.route('/')
    def index():
        return render_template('login.html')


    return app


# Ejecutar la aplicación
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
