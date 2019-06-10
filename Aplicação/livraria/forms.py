'''
livraria/forms.py

Define formularios usados na aplicação.
'''

from flask_wtf import FlaskForm
from wtforms import IntegerField, DecimalField, StringField, SubmitField, SelectField
from wtforms.validators import DataRequired as Data, Email, ValidationError
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
