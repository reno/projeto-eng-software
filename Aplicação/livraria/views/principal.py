"""
livraria/views/principal.py

Define rotas comuns a aplicação.
"""

from flask import Flask, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from livraria import app
from livraria.models import *
from livraria.tables import *
from livraria.forms.principal import *


@app.route('/')
@login_required
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = FormLogin()
    if form.validate_on_submit():
        usuario = Funcionario.query.filter_by(usuario=form.usuario.data).first()
        print(usuario)
        if usuario is not None and usuario.verifica_senha(form.senha.data):
            login_user(usuario, True)
            return redirect(url_for('index'))
        else:
            flash('Usuário ou senha incorretos.', category='danger')
    return render_template('login.html', form=form, header='Entrar')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você foi desconectado', category='message')
    return redirect(url_for('login'))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404