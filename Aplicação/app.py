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
    # ao enviar form, realiza consulta e renderiza resultados 
    if form.validate_on_submit():
        parametros = {form.campo.data: form.termo.data}
        resultado = Livro.query.filter_by(**parametros).all()
        tabela = TabelaLivros(resultado)
        return render_template('livros/resultado.html', table=tabela)
    # formulário ainda não enviado, renderiza página
    else:
        return render_template('livros/consultar.html', form=form)


@app.route('/livro/cadastrar', methods=['GET', 'POST'])
def cadastrar_livro():
    form = FormCadastroLivro()
    # ao enviar form, verifica se livro já existe no BD e cadastra
    if form.validate_on_submit():
        livro = Livro.query.filter_by(isbn=form.isbn.data).first()
        if livro is not None:
            return render_template('index.html', text='Livro {} já cadastrado.'.format(livro))
        else:
            dados = form.data
            del dados['submit']
            del dados['csrf_token']
            livro = Livro(**dados)
            db.session.add(livro)
            db.session.commit()            
            return render_template('index.html', text='Livro cadastrado com sucesso.')
    else:
        # formulário ainda não enviado, renderiza página
        return render_template('livros/consultar.html', form=form)


@app.route('/livro/atualizar', methods=['GET', 'POST'])
def atualizar_livro():
    #form = FormConsultaLivro()
    #form = FormCadastroLivro()
    return render_template('index.html', header='Atualizar livro')


@app.route('/livro/excluir', methods=['GET', 'POST'])
def excluir_livro():
    #form = FormConsultaLivro()
    return render_template('index.html', header='Excluir livro')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
