'''
livraria/forms.py

Define formularios usados na aplicação.
'''

from flask_wtf import FlaskForm
from wtforms import IntegerField, DecimalField, StringField, SubmitField, SelectField, BooleanField, PasswordField
from wtforms.validators import DataRequired as Data, Email, Regexp, EqualTo, ValidationError
from isbnlib import is_isbn10, is_isbn13
from livraria.models import *

MSG_USUARIO = 'O nome de usuário deve conter apenas letras minúsculas, números e underscore.'
MSG_SENHA = 'As senhas precisam ser idênticas.'

def isbn():
    '''Validator para o campo ISBN'''
    message = 'Informe um ISBN válido'
    def _isbn(form, field):
        if not is_isbn10(field.data) and not is_isbn13(field.data):
            raise ValidationError(message)
    return _isbn



class FormLogin(FlaskForm):
    usuario = StringField('Usuário', validators=[Data(), Regexp('^[a-z0-9_]+$', message=MSG_USUARIO)])
    senha = PasswordField('Senha', validators=[Data()])
    submit = SubmitField('Entrar')


class FormConsultaLivro(FlaskForm):
    opcoes = [(atr, atr.capitalize()) for atr in dir(Livro)
              if atr is not 'id' and not atr.startswith(('_', 'q', 'm'))]
    campo = SelectField('Campo de busca', choices=opcoes)  
    termo = StringField('Palavra-chave', validators=[Data()])
    submit = SubmitField('Consultar')


class FormCadastroLivro(FlaskForm):
    titulo = StringField('Título', validators=[Data()])
    autor = StringField('Autor', validators=[Data()])
    editora = StringField('Editora', validators=[Data()])
    edicao = StringField('Edição', validators=[Data()])
    ano = IntegerField('Ano', validators=[Data()])
    isbn = StringField('ISBN', validators=[Data()], id='isbn_field')#, isbn()], )
    idioma = StringField('Idioma', validators=[Data()])
    preco = DecimalField('Preço', validators=[Data()])
    exemplares = IntegerField('Número de exemplares', validators=[Data()])
    submit = SubmitField('Enviar')


class FormConsultaIsbn(FlaskForm):
    isbn = StringField('ISBN', validators=[Data()])#, isbn()])
    submit = SubmitField('Consultar')


class FormExclusaoLivro(FlaskForm):
    submit = SubmitField('Excluir')


class FormCadastroVendedor(FlaskForm):
    nome = StringField('Nome', validators=[Data()])
    usuario = StringField('Usuário', validators=[Data(), Regexp('^[a-z0-9_]+$', message=MSG_USUARIO)])
    senha  = PasswordField('Senha', validators=[Data(), EqualTo('confirma_senha', message=MSG_SENHA)])
    confirma_senha  = PasswordField('Confirme a senha', validators=[Data()])
    admin = BooleanField('Conceder permissão de administrador.')
    submit = SubmitField('Registrar')

    def validate_usuario(self, field):
        if Funcionario.query.filter_by(usuario=field.data).first():
            raise ValidationError('Nome de usuário já utilizado.')

