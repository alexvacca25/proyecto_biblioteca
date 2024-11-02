# models/book.py
from extensions import db

class Book(db.Model):
    __tablename__ = 'book'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False, unique=True)  # Título del libro
    author = db.Column(db.String(100), nullable=False)  # Autor del libro
     
    available = db.Column(db.Boolean, default=True)  # Indica si el libro está disponible para préstamo
    loaned_count = db.Column(db.Integer, default=0)  # Contador de préstamos realizados
    anno_publica=db.Column(db.Integer,nullable=False)
    serie=db.Column(db.String(100),unique=True,nullable=False)
    
    def __repr__(self):
        return f"<Book {self.title} by {self.author}>"

    def mark_as_loaned(self):
        """Marca el libro como prestado."""
        self.available = False
        self.loaned_count += 1

    def mark_as_returned(self):
        """Marca el libro como disponible."""
        self.available = True
