'''
livraria/forms/principal.py

Define formularios usados na aplicacao.
'''

from flask_wtf import FlaskForm
from wtforms import IntegerField, DecimalField, StringField, SubmitField, SelectField, BooleanField, PasswordField
from wtforms.validators import DataRequired as Data, Email, Regexp, EqualTo, ValidationError
#from isbnlib import is_isbn10, is_isbn13
#from livraria.models import *

MSG_USUARIO = 'O nome de usuário deve conter apenas letras minúsculas, números e underscore.'


class FormLogin(FlaskForm):
    usuario = StringField('Usuário', validators=[Data(), Regexp('^[a-z0-9_]+$', message=MSG_USUARIO)])
    senha = PasswordField('Senha', validators=[Data()])
    submit = SubmitField('Entrar')
