'''
livraria/forms.py

Define formularios usados na aplicação.
'''

from flask_wtf import FlaskForm
from wtforms import IntegerField, DecimalField, StringField, SubmitField, SelectField
from wtforms.validators import InputRequired as Req, Email, ValidationError
from isbnlib import is_isbn10, is_isbn13
from livraria.models import *


def isbn():
    '''Validator para o campo ISBN'''
    message = 'Informe um ISBN válido'
    def _isbn(form, field):
        if not is_isbn10(field.data) and not is_isbn13(field.data):
            raise ValidationError(message)
    return _isbn


class FormConsultaLivro(FlaskForm):
    opcoes = [(atr, atr.capitalize()) for atr in dir(Livro)
              if atr is not 'id' and not atr.startswith(('_', 'q', 'm'))]
    campo = SelectField('Campo de busca', choices=opcoes)  
    termo = StringField('Palavra-chave', validators=[Req()])
    submit = SubmitField('Consultar')


class FormCadastroLivro(FlaskForm):
    titulo = StringField('Título', validators=[Req()])
    autor = StringField('Autor', validators=[Req()])
    editora = StringField('Editora', validators=[Req()])
    edicao = StringField('Edição', validators=[Req()])
    ano = IntegerField('Ano', validators=[Req()])
    isbn = StringField('ISBN', validators=[Req()], id='isbn_field')#, isbn()], )
    idioma = StringField('Idioma', validators=[Req()])
    preco = DecimalField('Preço', validators=[Req()])
    exemplares = IntegerField('Número de exemplares', validators=[Req()])
    submit = SubmitField('Enviar')


class FormConsultaIsbn(FlaskForm):
    isbn = StringField('ISBN', validators=[Req()])#, isbn()])
    submit = SubmitField('Consultar')


class FormExclusaoLivro(FlaskForm):
    submit = SubmitField('Excluir')
