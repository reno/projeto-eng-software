'''
livraria/views/livro.py

Define rotas do menu Livro.
'''

from flask import Flask, render_template, redirect, url_for, request, session
from flask_login import login_required
from isbnlib import is_isbn10, is_isbn13, mask, canonical, meta
from livraria.models import *
from livraria.tables import *
from livraria.forms.livro import *
from livraria import app


@app.route('/livro/consultar', methods=['GET', 'POST'])
@login_required
def consultar_livro():
    form = FormConsultaLivro()
    # ao enviar form, realiza consulta e renderiza resultados 
    if form.validate_on_submit():
        parametros = {form.campo.data: form.termo.data}
        resultado = Livro.query.filter_by(**parametros).all()
        tabela = TabelaLivros(resultado)
        return render_template('livro/resultado.html', table=tabela)
    # formulário ainda não enviado, renderiza página
    else:
        return render_template('livro/consultar.html', form=form, header='Consultar livro')


@app.route('/livro/cadastrar', methods=['GET', 'POST'])
@login_required
def cadastrar_livro():
    form = FormCadastroLivro()
    # ao enviar form, verifica se livro já existe no BD e cadastra
    if form.validate_on_submit():
        livro = Livro.query.filter_by(isbn=form.isbn.data).first()
        if livro is not None:
            return render_template('livro/index.html', text='Livro {} já cadastrado.'.format(mask(str(livro))))
        else:
            dados = {k: v for k, v in form.data.items()
                     if k not in {'submit','csrf_token'}}
            livro = Livro(**dados)
            #livro['isbn'] = canonical(livro['isbn'])
            db.session.add(livro)
            db.session.commit()
            return render_template('livro/index.html', text='Livro {} cadastrado com sucesso.'.format(mask(str(livro))))
    # formulário ainda não enviado, renderiza página
    else:
        return render_template('livro/cadastrar.html', form=form, header='Cadastrar livro')


@app.route('/livro/<op>/consulta', methods=['GET', 'POST'])
@login_required
def consultar_isbn(op):
    form_isbn = FormConsultaIsbn()
    # consulta realizada, redireciona conforme operação 
    if form_isbn.validate_on_submit():
        livro = Livro.query.filter_by(isbn=form_isbn.isbn.data).first()
        if livro is None:
            return render_template('livro/index.html', text='Nenhum livro encontrado.')    
        if op == 'atualizar':
            return redirect(url_for('atualizar_livro', isbn=livro.isbn))
        else:
            return redirect(url_for('excluir_livro', isbn=livro.isbn))
    # formulário ainda não enviado, renderiza página
    else: 
        return render_template('livro/isbn.html', form=form_isbn, header='{} livro'.format(op.capitalize()))

    
@app.route('/livro/atualizar/', methods=['GET', 'POST'])
@login_required
def atualizar_livro(): 
    isbn = request.args['isbn']
    livro = Livro.query.filter_by(isbn=isbn).first()
    form_atualizacao = FormCadastroLivro(obj=livro)
    form_atualizacao.populate_obj(livro)
    if form_atualizacao.validate_on_submit():
        dados = {k: v for k, v in form_atualizacao.data.items()
                 if k not in {'submit','csrf_token'}}
        livro.data = dados 
        db.session.commit()
        return render_template('livro/index.html', text='Livro atualizado com sucesso.')  
    # formulário ainda não enviado, renderiza página
    else:
        return render_template('livro/atualizar.html', form=form_atualizacao, header='Atualizar livro') 


@app.route('/livro/excluir/', methods=['GET', 'POST'])
@login_required
def excluir_livro():
    isbn = request.args['isbn']
    resultado = Livro.query.filter_by(isbn=isbn).all()
    tabela = TabelaLivros(resultado)
    livro = resultado[0]
    confirmacao = FormExclusaoLivro()
    if confirmacao.validate_on_submit():
        db.session.delete(livro)
        db.session.commit()
        return render_template('livro/index.html', text='Livro excluido com sucesso.')
    else:
        return render_template('livro/excluir.html', table=tabela, form=confirmacao, header='Excluir livro')
