'''
livraria/models.py

Define tabelas do banco de dados. Para criação do BD, execute o script 'create_db.py'
'''

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


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

class Funcionario(db.Model):
    registro = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String)
    usuario = db.Column(db.String, unique=True)
    senha_hash = db.Column(db.String(128))
    admin = db.Column(db.Boolean)

    @property
    def senha(self):
        raise AttributeError('senha não é um atributo acessível')

    @senha.setter
    def senha(self, senha):
        self.senha_hash = generate_password_hash(senha)

    def verifica_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)

    def __repr__(self):
        return self.usuario



