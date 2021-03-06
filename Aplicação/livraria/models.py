"""
livraria/models.py

Define tabelas do banco de dados.
Para criação do BD, execute o script 'create_db.py'
"""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager

db = SQLAlchemy()

class Livro(db.Model):
    """Define a tabela Livros no banco de dados"""
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
    pedidos = db.relationship('ItemPedido', backref='livros',
                              cascade='all, delete-orphan')

    def __repr__(self):
        return self.isbn


class Funcionario(UserMixin, db.Model):
    """Define a tabela Funcionarios no banco de dados"""
    __tablename__ = "funcionarios"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)
    usuario = db.Column(db.String, unique=True, nullable=False)
    senha_hash = db.Column(db.String(128))
    admin = db.Column(db.Boolean)
    __mapper_args__ = {'polymorphic_on': 'admin'}

    @property
    def senha(self):
        raise AttributeError('senha não é um atributo acessível')

    @senha.setter
    def senha(self, senha):
        self.senha_hash = generate_password_hash(senha)

    def verifica_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)

    def is_admin(self):
        return self.admin

    def __repr__(self):
        return self.usuario


VENDEDOR = False
ADMIN = True

class Vendedor(Funcionario):
    """Estende a tabela Funcionarios"""
    __mapper_args__ = {'polymorphic_identity': VENDEDOR}

class Admin(Funcionario):
    """Estende a tabela Funcionarios"""
    __mapper_args__ = {'polymorphic_identity': ADMIN}


@login_manager.user_loader
def load_user(user_id):
    return Funcionario.query.get(int(user_id))


class Cliente(db.Model):
    """Define a tabela Clientes no banco de dados"""
    __tablename__ = "clientes"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)
    documento = db.Column(db.String, nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    endereco = db.relationship('Endereco', cascade="all,delete",
                                backref='cliente', lazy=True,
                                uselist=False)
    telefone = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)

    def __repr__(self):
        return self.documento


class Endereco(db.Model):
    """Representa o endereço de um cliente."""
    __tablename__ = "enderecos"
    id = db.Column(db.Integer, primary_key=True)
    logradouro = db.Column(db.String, nullable=False)
    numero = db.Column(db.String, nullable=False)
    complemento = db.Column(db.String)
    bairro = db.Column(db.String, nullable=False)
    cidade = db.Column(db.String, nullable=False)
    estado = db.Column(db.String, nullable=False)
    cep = db.Column(db.String, nullable=False)
    id_cliente = db.Column(db.Integer, db.ForeignKey('clientes.id'),
                           nullable=False)
    
    def __repr__(self):
        return '{}, {} {}, {} - {}'.format(self.logradouro, self.numero,
                                           self.complemento, self.bairro,
                                           self.cidade)


pedidos_cliente = db.Table('pedidos_cliente',
    db.Column('id_pedido', db.Integer, db.ForeignKey('pedidos.id')),
    db.Column('id_cliente', db.Integer, db.ForeignKey('clientes.id'))
)

pedidos_vendedor = db.Table('pedidos_vendedor',
    db.Column('id_pedido', db.Integer, db.ForeignKey('pedidos.id')),
    db.Column('id_vendedor', db.Integer, db.ForeignKey('funcionarios.id'))
)


class Pedido(db.Model):
    """Define a tabela Pedidos no banco de dados"""
    __tablename__ = "pedidos"
    id = db.Column(db.Integer, primary_key=True)
    itens = db.relationship('ItemPedido', backref='pedidos', lazy=True,
                            cascade='all, delete')
    cliente = db.relationship('Cliente', secondary=pedidos_cliente,
                              backref='pedidos', lazy=True, uselist=False)
    vendedor = db.relationship('Funcionario', secondary=pedidos_vendedor,
                               backref='pedidos', lazy=True, uselist=False)
    desconto = db.Column(db.Integer, default=0, nullable=False)
    total = db.Column(db.Float)
    ativo = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return str(self.id)


class ItemPedido(db.Model):
    """Representa um item de um pedido. """
    __tablename__ = "itens_pedido"
    id_pedido = db.Column(db.Integer, db.ForeignKey('pedidos.id'),
                          primary_key=True)
    id_livro = db.Column(db.Integer, db.ForeignKey('livros.id'),
                         primary_key=True)
    quantidade = db.Column(db.Integer, nullable=False)
    livro = db.relationship('Livro', backref='pedido')
    pedido = db.relationship('Pedido', backref='livro')

    def __repr__(self):
        return f'{self.livro} {self.quantidade}'
