from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from models import *
from forms import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost/livraria'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = 'string de verificacao do flask-wtf'

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
db.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/livro/consultar', methods=['GET', 'POST'])
def consultar_livro():
    form = FormConsultaLivro()
    if form.validate_on_submit():
        livro = Livro.query.filter_by(isbn=form.isbn)
        return str(livro)
    else:
        return render_template('consultar_livro.html', form=form)


@app.route('/livro/cadastrar', methods=['GET', 'POST'])
def cadastrar_livro():
    return '<h1>cadastrar livro</h1>'


@app.route('/livro/atualizar', methods=['GET', 'POST'])
def atualizar_livro():
    return '<h1>atualizar livro</h1>'


@app.route('/livro/excluir', methods=['GET', 'POST'])
def excluir_livro():
    return '<h1>excluir livro</h1>'


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
