'''
livraria/forms/admin.py

Define formularios usados no menu Admin.
'''

from flask_wtf import FlaskForm
from wtforms import IntegerField, DecimalField, StringField, SubmitField, SelectField, BooleanField, PasswordField
from wtforms.validators import DataRequired as Data, Email, Regexp, EqualTo, ValidationError
from isbnlib import is_isbn10, is_isbn13
from livraria.models import *

MSG_USUARIO = 'O nome de usuário deve conter apenas letras minúsculas, números e underscore.'
MSG_SENHA = 'As senhas precisam ser idênticas.'


class FormConsultaVendedor(FlaskForm):
    opcoes = [(atr, atr.capitalize()) for atr in dir(Funcionario)
              if atr is not 'id' and not atr.startswith(('_', 'a', 'q', 'm', 'v', 'is', 'senha', 'get'))]
    opcoes.insert(0, ('id', 'Registro'))
    campo = SelectField('Campo de busca', choices=opcoes)  
    termo = StringField('Palavra-chave', validators=[Data()])
    submit = SubmitField('Consultar')


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


class FormConsultaId(FlaskForm):
    id = StringField('Nº registro', validators=[Data()])
    submit = SubmitField('Localizar')


class FormExclusaoVendedor(FlaskForm):
    submit = SubmitField('Excluir')


class FormExclusaoCliente(FlaskForm):
    submit = SubmitField('Excluir')
