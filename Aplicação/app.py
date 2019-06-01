from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from models import *
from forms import *
from tables import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost/livraria'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = 'string de verificacao do flask-wtf'

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
db.init_app(app)


@app.route('/')
def index():
    return render_template('index.html', header='Bem vindo!')


@app.route('/livros/consultar', methods=['GET', 'POST'])
def consultar_livro():
    form = FormConsultaLivro()
    # ao enviar form, realiza consulta e redireciona
    if form.validate_on_submit():
        opcao = form.campo.data
        if opcao == 'isbn':
            resultado = Livro.query.filter_by(isbn=form.termo.data).all()
        else:
            resultado = Livro.query.filter_by(titulo=form.termo.data).all()
        tabela = TabelaLivros(resultado)
        #return redirect(url_for('resultado_livros', tabela=tabela))
        return render_template('livros/resultado.html', table=tabela)
    # renderiza pagina
    else:
        return render_template('livros/consultar.html', form=form)

'''
@app.route('/livros/consultar/resultado')
def resultado_livros():
    return render_template('livros/resultado.html',
                           table=request.args.get('tabela'))
'''

@app.route('/livro/cadastrar', methods=['GET', 'POST'])
def cadastrar_livro():
    form = FormCadastroLivro()
    if form.validate_on_submit():
        pass
    return render_template('livros/consultar.html', form=form)


@app.route('/livro/atualizar', methods=['GET', 'POST'])
def atualizar_livro():
    form = FormConsultaLivro()
    #form = FormCadastroLivro()
    return render_template('livros/atualizar.html', form=form)


@app.route('/livro/excluir', methods=['GET', 'POST'])
def excluir_livro():
    form = FormConsultaLivro()
    return render_template('livros/excluir.html', form=form)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
