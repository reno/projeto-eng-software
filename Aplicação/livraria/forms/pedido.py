'''
livraria/forms/pedido.py

Define formularios usados no menu Pedidos.
'''

from flask_wtf import FlaskForm
from wtforms import IntegerField, DecimalField, StringField, SubmitField, SelectField, FieldList, FormField, BooleanField, HiddenField
from wtforms.validators import DataRequired as Data, Email, Regexp, ValidationError
from isbnlib import is_isbn10, is_isbn13
from livraria.models import *


class FormItensPedido(FlaskForm):
    livro = StringField('Livro', validators=[Data()])
    quantidade = IntegerField('Quantidade', validators=[Data()])

    def validate_livro(self, field):
        if not is_isbn10(field.data) and not is_isbn13(field.data):
            return ValidationError('ISBN inválido')
        if Livro.query.filter_by(isbn=field.data).first() is None:
            raise ValidationError('Livro não encontrado.')


class FormCadastroPedido(FlaskForm):
    cliente = StringField('Cliente', validators=[Data()])
    itens = FieldList(FormField(FormItensPedido), min_entries=1, max_entries=9)
    #vendedor = HiddenField()
    desconto = StringField('Desconto', validators=[Data()])
    #total = HiddenField()
    submit = SubmitField('Cadastrar')

    def validate_cliente(self, field):
        if Cliente.query.filter_by(documento=field.data).first() is None:
            raise ValidationError('Cliente não encontrado.')


class FormConsultaPedido(FlaskForm):
    opcoes = [('id', 'Nº pedido'), ('cliente', 'Cliente'), ('vendedor', 'Vendedor')]
    campo = SelectField('Campo de busca', choices=opcoes)  
    termo = StringField('Palavra-chave', validators=[Data()])
    consultar_ativos = BooleanField('Consultar somente pedidos ativos.')
    submit = SubmitField('Consultar')


class FormNumeroPedido(FlaskForm):
    pedido = StringField('Nº pedido', validators=[Data()])
    submit = SubmitField('Consultar')


class FormCancelamentoPedido(FlaskForm):
    submit = SubmitField('Excluir')

