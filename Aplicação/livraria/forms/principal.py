'''
livraria/forms/principal.py

Define formularios usados na aplicacao.
'''

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired as Data, Regexp

MSG_USUARIO = 'O nome de usuário deve conter apenas letras minúsculas, números e underscore.'


class FormLogin(FlaskForm):
    usuario = StringField('Usuário', validators=[Data(),
                          Regexp('^[a-z0-9_]+$', message=MSG_USUARIO)])
    senha = PasswordField('Senha', validators=[Data()])
    submit = SubmitField('Entrar')
