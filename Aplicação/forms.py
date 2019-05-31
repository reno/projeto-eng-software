from flask_wtf import FlaskForm
from wtforms import IntegerField, DecimalField, StringField, SubmitField
from wtforms.validators import DataRequired, Regexp, Email

class FormConsultaLivro(FlaskForm):
    nome = StringField()
    isbn = StringField()
    submit = SubmitField()
