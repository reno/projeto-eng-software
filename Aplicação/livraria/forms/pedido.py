"""
livraria/forms/pedido.py

Define formularios usados no menu Pedidos.
"""

from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import IntegerField, DecimalField, StringField, SubmitField,\
                    SelectField, FieldList, FormField, BooleanField, HiddenField
from wtforms.validators import DataRequired as Data,\
                               InputRequired, Email, Regexp, ValidationError
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
    desconto = IntegerField('Desconto', validators=[InputRequired()])
    submit = SubmitField('Cadastrar')

    def validate_cliente(self, field):
        if Cliente.query.filter_by(documento=field.data).first() is None:
            raise ValidationError('Cliente não encontrado.')


class FormAtualizacaoPedido(FlaskForm):
    id = HiddenField()
    cliente = StringField('Cliente', validators=[Data()])
    itens = FieldList(FormField(FormItensPedido))
    vendedor = HiddenField()
    desconto = IntegerField('Desconto', validators=[Data()])
    total = HiddenField()
    submit = SubmitField('Cadastrar')

    def validate_cliente(self, field):
        if Cliente.query.filter_by(documento=field.data).first() is None:
            raise ValidationError('Cliente não encontrado.')

    def populate(self, pedido):
        i = 0
        cliente = Cliente.query.filter_by(documento=self.cliente.data).first()
        pedido.cliente = cliente
        vendedor = Funcionario.query.filter_by(id=current_user.id).first()
        pedido.vendedor = vendedor
        pedido.desconto = self.desconto.data
        total = 0
        for item in pedido.itens:
            livro = Livro.query.filter_by(isbn=self.itens[i].livro.data).first()
            item.livro = livro
            item.quantidade = self.itens[i].quantidade.data
            total += livro.preco * item.quantidade
            i += 1
        pedido.total = total


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

