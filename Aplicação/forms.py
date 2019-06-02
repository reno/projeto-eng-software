from flask_wtf import FlaskForm
from wtforms import IntegerField, DecimalField, StringField, SubmitField, SelectField
from wtforms.validators import InputRequired as Req, Regexp, Email


class FormConsultaLivro(FlaskForm):
    campo = SelectField('Campo de busca', choices=[('isbn','ISBN'), ('titulo','Título')])
    termo = StringField('Palavra-chave', validators=[Req()])
    submit = SubmitField('Consultar')

class FormCadastroLivro(FlaskForm):
    titulo = StringField('Título', validators=[Req()])
    autor = StringField('Autor', validators=[Req()])
    editora = StringField('Editora', validators=[Req()])
    edicao = StringField('Edição', validators=[Req()])
    ano = IntegerField('Ano', validators=[Req()])
    isbn = StringField('ISBN', validators=[Req()])
    idioma = StringField('Idioma', validators=[Req()])
    preco = DecimalField('Preço', validators=[Req()])
    exemplares = IntegerField('Número de exemplares', validators=[Req()])
    submit = SubmitField('Enviar')

class FormConsultaIsbn(FlaskForm):
    isbn = StringField('ISBN', validators=[Req()])
    submit = SubmitField('Consultar')

class FormExclusaoLivro(FlaskForm):
    submit = SubmitField('Excluir')
