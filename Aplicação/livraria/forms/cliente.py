"""
livraria/forms/cliente.py

Define formularios usados no menu Clientes.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, FormField, SubmitField
from wtforms.validators import DataRequired as Data, Email, Regexp
from livraria.models import *

MSG_DOC = 'Informe apenas números do RG ou CPF.'
MSG_TEL = 'Informe apenas números, incluindo o DDD'
MSG_CEP = 'Informe apenas números'


class FormConsultaCliente(FlaskForm):
    opcoes = [(atr, atr.capitalize()) for atr in dir(Cliente)
              if not atr.startswith(('_', 'id', 'm', 'q', 'data'))]
    campo = SelectField('Campo de busca', choices=opcoes)  
    termo = StringField('Palavra-chave', validators=[Data()])
    submit = SubmitField('Consultar')


class FormEndereco(FlaskForm):
    logradouro = StringField('Logradouro', validators=[Data()])
    numero = StringField('Número', validators=[Data()])
    complemento = StringField('Complemento')
    bairro = StringField('Bairro', validators=[Data()])
    cidade = StringField('Cidade', validators=[Data()])
    estado = StringField('Estado', validators=[Data()])
    cep = StringField('CEP', validators=[Data(), Regexp('^[0-9]{8}$',
                                         message=MSG_CEP)])


class FormCadastroCliente(FlaskForm):
    nome = StringField('Nome', validators=[Data()])
    documento = StringField('Documento', validators=[Data(),
                            Regexp('^[0-9]{5,13}$', message=MSG_DOC)])
    data_nascimento = DateField('Data de nascimento',
                                validators=[Data()], format='%d/%m/%Y')
    endereco = FormField(FormEndereco)
    telefone = StringField('Telefone', validators=[Data(),
                            Regexp('^[0-9]{10,11}$', message=MSG_TEL)])
    email = StringField('E-mail', validators=[Data(), Email()])
    submit = SubmitField('Cadastrar')


class FormConsultaDocumento(FlaskForm):
    documento = StringField('Documento', validators=[Data(),
                            Regexp('^[0-9]{5,13}$', message=MSG_DOC)])
    submit = SubmitField('Localizar')
