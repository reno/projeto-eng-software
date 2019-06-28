"""
livraria/views/cliente.py

Define rotas do menu Clientes.
"""

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from livraria import app
from livraria.models import *
from livraria.tables import *
from livraria.forms.cliente import *


@app.route('/cliente/consultar', methods=['GET', 'POST'])
@login_required
def consultar_cliente():
    form = FormConsultaCliente()
    # ao enviar form, realiza consulta e renderiza resultados
    if form.validate_on_submit():
        parametros = {form.campo.data: form.termo.data}
        resultado = Cliente.query.filter_by(**parametros).all()
        tabela = TabelaClientes(resultado)
        return render_template('cliente/resultado.html', table=tabela)
    # formulário ainda não enviado, renderiza página
    return render_template('cliente/consultar.html', form=form,
        header='Consultar cliente')


@app.route('/cliente/cadastrar', methods=['GET', 'POST'])
@login_required
def cadastrar_cliente():
    form = FormCadastroCliente()
    # ao enviar form, verifica se cliente já existe no BD e cadastra
    if form.validate_on_submit():
        cliente = Cliente.query.filter_by(documento=form.documento.data).first()
        if cliente is not None:
            return render_template('cliente/index.html',
                text='Cliente {} já cadastrado.'.format(cliente))
        else:
            dados_endereco = {k: v for k, v in form.endereco.data.items()
                              if k not in {'csrf_token'}}
            endereco = Endereco(**dados_endereco)
            dados = {k: v for k, v in form.data.items()
                     if k not in {'endereco', 'submit','csrf_token'}}
            cliente = Cliente(**dados)
            cliente.endereco = endereco
            db.session.add(cliente)
            db.session.commit()
            return render_template('cliente/index.html',
                text='Cliente {} cadastrado com sucesso.'.format(cliente))
    else:
        return render_template('cliente/cadastrar2.html', form=form,
            header='Cadastrar cliente') 


@app.route('/cliente/<op>/consulta', methods=['GET', 'POST'])
@login_required
def consultar_documento(op):
    form = FormConsultaDocumento()
    # consulta realizada, redireciona conforme operação 
    if form.validate_on_submit():
        cliente = Cliente.query.filter_by(documento=form.documento.data).first()
        if cliente is None:
            return render_template('cliente/index.html',
                text='Nenhum cliente encontrado.')    
        if op == 'atualizar':
            return redirect(url_for('atualizar_cliente', doc=cliente.documento))
        else:
            return redirect(url_for('excluir_cliente', doc=cliente.documento))
    # formulário ainda não enviado, renderiza página
    else:
        return render_template('cliente/cadastrar.html', form=form,
            header='{} cliente'.format(op.capitalize()))


@app.route('/cliente/atualizar', methods=['GET', 'POST'])
@login_required
def atualizar_cliente():
    documento = request.args['doc']
    cliente = Cliente.query.filter_by(documento=documento).first()
    form_atualizacao = FormCadastroCliente(obj=cliente)
    form_atualizacao.populate_obj(cliente)
    # ao enviar form, atualiza dados do cliente
    if form_atualizacao.validate_on_submit():
        dados = {k: v for k, v in form_atualizacao.data.items()
                 if k not in {'submit','csrf_token'}}
        cliente.data = dados 
        db.session.commit()
        return render_template('cliente/index.html',
            text='Cliente atualizado com sucesso.')
    # formulário ainda não enviado, renderiza página
    else:
        return render_template('cliente/cadastrar.html', form=form_atualizacao,
            header='Atualizar cliente') 