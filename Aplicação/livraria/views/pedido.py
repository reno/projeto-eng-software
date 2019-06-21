'''
livraria/views/pedido.py

Define rotas do menu Pedidos.
'''

from flask import Flask, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from livraria import app #, views
from livraria.models import *
from livraria.tables import *
from livraria.forms.pedido import *

@app.route('/pedido/consultar', methods=['GET', 'POST'])
@login_required
def consultar_pedido():
    pass

@app.route('/pedido/cadastrar', methods=['GET', 'POST'])
@login_required
def cadastrar_pedido():
    pass

@app.route('/pedido/atualizar', methods=['GET', 'POST'])
@login_required
def atualizar_pedido():
    pass

@app.route('/pedido/cancelar', methods=['GET', 'POST'])
@login_required
def cancelar_pedido():
    pass


