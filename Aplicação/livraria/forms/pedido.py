'''
livraria/forms/pedido.py

Define formularios usados no menu Pedidos.
'''

from flask_wtf import FlaskForm
from wtforms import IntegerField, DecimalField, StringField, SubmitField, SelectField, FieldList, FormField
from wtforms.validators import DataRequired as Data, Email, Regexp, ValidationError
from isbnlib import is_isbn10, is_isbn13
from livraria.models import *


class FormItensPedido(FlaskForm):
    livro = StringField('Livro', validators=[Data()])
    quantidade = IntegerField('Quantidade', validators=[Data()])

    def validate_livro(self, field):
        if not is_isbn10(field.data) and not is_isbn13(field.data):
            return ValidationError('ISBN inválido')
        if not Livro.query.filter_by(isbn=field.data).first():
            raise ValidationError('Livro não encontrado.')


class FormCadastroPedido(FlaskForm):
    cliente = StringField('Cliente', validators=[Data()])
    itens = FieldList(FormField(FormItensPedido), min_entries=1, max_entries=99)
    vendedor = StringField('Vendedor', validators=[Data()])
    desconto = StringField('Desconto', validators=[Data()])
    total = StringField('Valor total', validators=[Data()])

    def validate_cliente(self, field):
        if not Cliente.query.filter_by(documento=field.data).first():
            raise ValidationError('Cliente não encontrado.')

    def validate_vendedor(self, field):
        if not Funcionario.query.filter_by(id=field.data).first():
            raise ValidationError('Vendedor não encontrado')


class FormConsultaPedido(FlaskForm):
    opcoes = [(atr, atr.capitalize()) for atr in dir(Pedido)
              if atr is not 'id' and not atr.startswith(('_'))]
    campo = SelectField('Campo de busca', choices=opcoes)  
    termo = StringField('Palavra-chave', validators=[Data()])
    submit = SubmitField('Consultar')


class FormNumeroPedido(FlaskForm):
    pedido = StringField('Nº pedido', validators=[Data()])
    submit = SubmitField('Consultar')


class FormExclusaoPedido(FlaskForm):
    submit = SubmitField('Excluir')

