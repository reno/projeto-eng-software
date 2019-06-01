from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Livro(db.Model):
    __tablename__ = "livros"
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String, nullable=False)
    autor = db.Column(db.String, nullable=False)
    editora = db.Column(db.String, nullable=False)
    edicao = db.Column(db.Integer, nullable=False)
    ano = db.Column(db.Integer, nullable=False)
    isbn = db.Column(db.String, nullable=False, unique=True)
    idioma = db.Column(db.String, nullable=False)
    preco = db.Column(db.Float, nullable=False)
    exemplares = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return self.isbn