'''
livraria/views/admin.py

Define rotas do menu Admin.
'''

from flask import Flask, render_template, url_for, flash
from flask_login import login_required
from livraria import app, views
from livraria.models import *
from livraria.forms import *
from livraria.tables import *
from livraria.decorators import admin_required


@app.route('/admin/cadastrar_vendedor', methods=['GET', 'POST'])
@login_required
@admin_required
def cadastrar_vendedor():
    form = FormCadastroVendedor()
    if form.validate_on_submit():
        vendedor = Funcionario.query.filter_by(usuario=form.usuario.data).first()
        if vendedor is not None:
            return render_template('index.html', text='Vendedor {} já cadastrado.'.format(vendedor))
        else:
            dados = {k: v for k, v in form.data.items()
                     if k not in {'submit','csrf_token','confirma_senha'}}
            vendedor = Funcionario(**dados)
            db.session.add(vendedor)
            db.session.commit()
            return render_template('index.html', text='Vendedor {} cadastrado com sucesso.'.format(vendedor))
    # formulário ainda não enviado, renderiza página
    else:
        return render_template('admin/admin.html', form=form, header='Cadastrar vendedor')
