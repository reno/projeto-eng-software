'''
livraria/models.py

Define tabelas do banco de dados.
Para criação do BD, execute o script 'create_db.py'
'''

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager

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


class Funcionario(UserMixin, db.Model):
    __tablename__ = "funcionarios"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String)
    usuario = db.Column(db.String, unique=True)
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

ADMIN = True
VENDEDOR = False

class Vendedor(Funcionario):
    __mapper_args__ = {'polymorphic_identity': VENDEDOR}

class Admin(Funcionario):
    __mapper_args__ = {'polymorphic_identity': ADMIN}

@login_manager.user_loader
def load_user(user_id):
    return Funcionario.query.get(int(user_id))


class Cliente(db.Model):
    __tablename__ = "clientes"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)
    documento = db.Column(db.String, nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    endereco = db.relationship('Endereco', cascade="all,delete", backref='cliente', lazy=True, uselist=False)
    telefone = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)

    def __repr__(self):
        return self.documento


class Endereco(db.Model):
    __tablename__ = "enderecos"
    id = db.Column(db.Integer, primary_key=True)
    logradouro = db.Column(db.String, nullable=False)
    numero = db.Column(db.String, nullable=False)
    complemento = db.Column(db.String)
    bairro = db.Column(db.String, nullable=False)
    cidade = db.Column(db.String, nullable=False)
    estado = db.Column(db.String, nullable=False)
    cep = db.Column(db.String, nullable=False)
    id_cliente = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    

itens_pedido = db.Table('itens_pedido',
    db.Column('id_livro', db.Integer, db.ForeignKey('livros.id'), primary_key=True),
    db.Column('quantidade', db.Integer),
    db.Column('id_pedido', db.Integer, db.ForeignKey('pedidos.id'), primary_key=True)
)


class Pedido(db.Model):
    __tablename__ = "pedidos"
    id = db.Column(db.Integer, primary_key=True)
    itens = db.relationship('Livro', secondary=itens_pedido, lazy='subquery',
                            backref=db.backref('pedidos', lazy=True))
    #id_item = db.Column(db.ARRAY(db.Integer), db.ForeignKey('itens_pedido.id'))
    id_cliente = db.Column(db.Integer, db.ForeignKey('clientes.id'))
    id_vendedor = db.Column(db.Integer, db.ForeignKey('funcionarios.id'))
    desconto = db.Column(db.Float, nullable=False)
    _valor_total = db.Column(db.Float, nullable=False)
    ativo = db.Column(db.Boolean)

    '''
    @hybrid_property
    def valor_total(self):
        _valor_total = sum([valor_item(i) for i in id_item])

    #@valor_item.expression
    def valor_item(id_item):
        return ItemPedido.query.get(id_item).quantidade * Livro.query.get(id_item).preco
    '''
    def __repr__(self):
        return self.id

