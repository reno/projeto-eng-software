'''
livraria/views/pedido.py

Define rotas do menu Pedidos.
'''

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from livraria import app
from livraria.models import *
from livraria.tables import *
from livraria.forms.pedido import *


@app.route('/pedido/consultar', methods=['GET', 'POST'])
@login_required
def consultar_pedido():
    form = FormConsultaPedido()
    # ao enviar form, realiza consulta e renderiza resultados
    if form.validate_on_submit():
        # realiza consultas necessárias e localiza pedido com dados informados
        # consultas com dados inválidos são redirecionadas
        if form.campo.data == 'cliente':
            cliente = Cliente.query.filter_by(documento=form.termo.data).first()
            if cliente is None:
                return render_template('pedido/index.html',
                                       text='Cliente não encontrado.')
            parametros = {'id_cliente': cliente.id}
        elif form.campo.data == 'vendedor':
            vendedor = Funcionario.query.filter_by(usuario=form.termo.data).first()
            if vendedor is None:
                return render_template('pedido/index.html',
                       text='Vendedor não encontrado.')
            parametros = {'id_vendedor': vendedor.id}
        else:  # pesquisa por id
            parametros = {'id': form.termo.data}
        if form.consultar_ativos.data is True:
            parametros['ativo'] = True
        print('PARAMETROS:', parametros)
        resultado = Pedido.query.filter_by(**parametros).all()
        tabela = TabelaPedidos(resultado)
        return render_template('pedido/resultado.html', table=tabela)
    # formulário ainda não enviado, renderiza página
    else:
        return render_template('pedido/consultar.html', form=form,
               header='Consultar pedido')


@app.route('/pedido/adicionar_item', methods=['GET', 'POST'])
@login_required
def adicionar_item(n):
    n += 1
    return render_template('pedido/cadastrar2.html', form=form, linhas=n,
           header='Cadastrar pedido')



@app.route('/pedido/cadastrar', methods=['GET', 'POST'])
@login_required
def cadastrar_pedido():
    form = FormCadastroPedido()
    # ao enviar form, verifica se pedido já existe no BD e cadastra
    if form.validate_on_submit():
        # obtem os dados do pedido
        dados = {k: v for k, v in form.data.items()
                 if k not in {'submit','csrf_token','itens', 'cliente'}}
        cliente = Cliente.query.filter_by(documento=form.cliente.data).first()
        dados['cliente'] = cliente
        vendedor = Funcionario.query.filter_by(id=current_user.id).first()
        dados['vendedor'] = vendedor
        # insere o pedido do BD
        pedido = Pedido(**dados)
        db.session.add(pedido)
        db.session.commit()
        # obtem os itens do pedido
        with db.session.no_autoflush:
            for linha in form.itens:
                livro = Livro.query.filter_by(isbn=linha.livro.data).first()
                quantidade = linha.quantidade.data
                item = ItemPedido(quantidade=quantidade)
                item.livro = livro
                pedido.itens.append(item)
        total = sum([item.livro.preco * item.quantidade for item in pedido.itens])
        pedido.total = total
        db.session.add(pedido)
        db.session.commit()
        return render_template('pedido/index.html',
               text= f'Pedido {pedido} cadastrado com sucesso. '
               + f'Valor total {pedido.total}')
    else:
        return render_template('pedido/cadastrar.html', form=form,
               header='Cadastrar pedido')


@app.route('/pedido/<op>/consulta', methods=['GET', 'POST'])
@login_required
def consultar_id(op):
    form = FormNumeroPedido()
    # consulta realizada, redireciona conforme operação 
    if form.validate_on_submit():
        pedido = Pedido.query.filter_by(id=form.pedido.data).first()
        if pedido is None:
            return render_template('pedido/index.html',
                   text='Nenhum pedido encontrado.')    
        if op == 'atualizar':
            return redirect(url_for('atualizar_pedido', id=pedido.id))
        else:
            return redirect(url_for('cancelar_pedido', id=pedido.id))
    else:
        return render_template('pedido/consultar.html', form=form,
               header=f'{op.capitalize()} pedido')


@app.route('/pedido/atualizar', methods=['GET', 'POST'])
@login_required
def atualizar_pedido():
    #if request.method == 'GET':
    id_pedido = request.args['id']
    pedido = Pedido.query.filter_by(id=id_pedido).first()
    if request.method == 'POST':
        form = FormAtualizacaoPedido()
        # ao enviar form, atualiza dados do pedido
        if form.validate_on_submit():
            form.populate(pedido)
            db.session.add(pedido)
            db.session.commit()
            return render_template('pedido/index.html',
                   text='Pedido atualizado com sucesso.')

    form = FormAtualizacaoPedido(obj=pedido)
    return render_template('pedido/cadastrar.html',
           form=form, header='Atualizar pedido')


@app.route('/pedido/cancelar', methods=['GET', 'POST'])
@login_required
def cancelar_pedido():
    id_pedido = request.args['id']
    resultado = Pedido.query.filter_by(id=id_pedido).all()
    tabela = TabelaPedidos(resultado)
    pedido = resultado[0]
    confirmacao = FormCancelamentoPedido()
    if confirmacao.validate_on_submit():
        pedido.ativo = False
        db.session.commit()
        return render_template('pedido/index.html',
               text= f'Pedido {pedido} cancelado com sucesso.')
    else:
        return render_template('pedido/cancelar.html', table=tabela,
               form=confirmacao, header='Cancelar pedido')


