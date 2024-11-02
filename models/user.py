# models/user.py
from extensions import db

class User(db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    first_name=db.Column(db.String(100),nullable=False)
    last_name=db.Column(db.String(100),nullable=False)
    address=db.Column(db.String(200),nullable=False)
    phone=db.Column(db.String(100),nullable=False)
    role = db.Column(db.Boolean, default=False)  # False = Usuario regular, True = Administrador
    
    # Relación con Loan
    loans = db.relationship('Loan', back_populates='user', lazy=True)

    def __repr__(self):
        return f"<User {self.username}>"
