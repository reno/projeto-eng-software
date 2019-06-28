"""
livraria/views/admin.py

Define rotas do menu Admin.
"""

from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from livraria import app
from livraria.models import *
from livraria.tables import *
from livraria.forms.admin import *
from livraria.decorators import admin_required


@app.route('/admin/consultar_vendedor', methods=['GET', 'POST'])
@login_required
@admin_required
def consultar_vendedor():
    form = FormConsultaVendedor()
    # ao enviar form, realiza consulta e renderiza resultados
    if form.validate_on_submit():
        parametros = {form.campo.data: form.termo.data}
        resultado = Vendedor.query.filter_by(**parametros).all()
        tabela = TabelaFuncionarios(resultado)
        return render_template('admin/resultado.html', table=tabela)
    # formulário ainda não enviado, renderiza página
    return render_template('admin/consultar.html', form=form,
                            header='Consultar vendedor')


@app.route('/admin/cadastrar_vendedor', methods=['GET', 'POST'])
@login_required
@admin_required
def cadastrar_vendedor():
    form = FormCadastroVendedor()
    if form.validate_on_submit():
        vendedor = Funcionario.query.filter_by(usuario=form.usuario.data).first()
        if vendedor is not None:
            return render_template('index.html',
                text='Vendedor {} já cadastrado.'.format(vendedor))
        else:
            dados = {k: v for k, v in form.data.items()
                     if k not in {'submit','csrf_token','confirma_senha'}}
            vendedor = Funcionario(**dados)
            db.session.add(vendedor)
            db.session.commit()
            return render_template('admin/index.html',
                text='Vendedor {} cadastrado com sucesso.'.format(vendedor))
    # formulário ainda não enviado, renderiza página
    else:
        return render_template('admin/cadastrar.html', form=form,
            header='Cadastrar vendedor')

@app.route('/admin/<op>/consulta', methods=['GET', 'POST'])
@login_required
@admin_required
def consultar_registro(op):
    form_registro = FormConsultaId()
    # consulta realizada, redireciona conforme operação 
    if form_registro.validate_on_submit():
        funcionario = Funcionario.query.filter_by(id=form_registro.id.data).first()
        if funcionario is None:
            return render_template('admin/index.html',
                text='Nenhum vendedor encontrado.')    
        if op == 'atualizar':
            return redirect(url_for('atualizar_vendedor', id=funcionario.id))
        else:
            return redirect(url_for('excluir_vendedor', id=funcionario.id))
    # formulário ainda não enviado, renderiza página
    else: 
        return render_template('admin/cadastrar.html', form=form_registro, 
            header='{} vendedor'.format(op.capitalize()))


@app.route('/admin/atualizar_dados')
@login_required
@admin_required
def atualizar_dados():
    return redirect(url_for('atualizar_vendedor', id=current_user.id))


@app.route('/admin/atualizar_vendedor', methods=['GET', 'POST'])
@login_required
@admin_required
def atualizar_vendedor():
    registro = request.args['id']
    funcionario = Funcionario.query.filter_by(id=registro).first()
    form = FormAtualizacaoVendedor(obj=funcionario)
    form.populate_obj(funcionario)
    if form.validate_on_submit():
        dados = {k: v for k, v in form.data.items()
                 if k not in {'submit','csrf_token', 'confirma_senha'}}
        funcionario.data = dados
        if form.nova_senha.data is not None:
            funcionario.senha = form.nova_senha.data
        db.session.add(funcionario)
        db.session.commit()
        return render_template('admin/index.html',
            text='Vendedor atualizado com sucesso.')  
    # formulário ainda não enviado, renderiza página
    else:
        return render_template('admin/cadastrar.html', form=form)


@app.route('/admin/excluir_vendedor', methods=['GET', 'POST'])
@login_required
@admin_required
def excluir_vendedor():
    registro = request.args['id']
    resultado = Funcionario.query.filter_by(id=registro).all()
    tabela = TabelaFuncionarios(resultado)
    funcionario = resultado[0]
    confirmacao = FormExclusaoVendedor()
    if confirmacao.validate_on_submit():
        db.session.delete(funcionario)
        db.session.commit()
        return render_template('admin/index.html',
            text='Vendedor excluido com sucesso.')
    else:
        return render_template('admin/excluir.html', table=tabela,
            form=confirmacao, header='Excluir vendedor')


@app.route('/admin/excluir_cliente', methods=['GET', 'POST'])
@login_required
@admin_required
def excluir_cliente():
    documento = request.args['doc']
    resultado = Cliente.query.filter_by(documento=documento).all()
    tabela = TabelaClientes(resultado)
    cliente = resultado[0]
    confirmacao = FormExclusaoCliente()
    if confirmacao.validate_on_submit():
        db.session.delete(cliente)
        db.session.commit()
        return render_template('admin/index.html',
            text='Cliente excluido com sucesso.')
    else:
        return render_template('admin/excluir.html', table=tabela,
            form=confirmacao, header='Excluir cliente')
    