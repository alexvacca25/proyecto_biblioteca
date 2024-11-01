# models/loan.py
from extensions import db
from datetime import datetime

class Loan(db.Model):
    __tablename__ = 'loan'
    
    id = db.Column(db.Integer, primary_key=True)
    loan_date = db.Column(db.DateTime, default=datetime.now)
    return_date = db.Column(db.DateTime, nullable=True)
    is_returned = db.Column(db.Boolean, default=False)
    
    # Relaciones de clave foránea
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)

    # Relaciones con modelos
    user = db.relationship('User', back_populates='loans')
    book = db.relationship('Book', backref='loans')

    def mark_as_loaned(self):
        """Marca el libro como prestado."""
        self.is_returned = False

    def mark_as_returned(self):
        """Marca el libro como disponible."""
        self.is_returned = True
