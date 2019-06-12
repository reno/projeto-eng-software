
from flask import Flask, render_template, url_for, flash
from flask_login import login_user, login_user, login_required
from livraria import app, views
from livraria.models import *
from livraria.forms import *
from livraria.tables import *


@app.route('/')
def index():
    return render_template('index.html', header='Bem vindo!')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = FormLogin()
    if form.validate_on_submit():
        usuario = Funcionario.query.filter_by(usuario=form.usuario.data).first()
        if usuario is not None and usuario.verify_password(form.senha.data):
            login_user(usuario)
            return redirect('index')
            '''
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('index')
            return redirect(next)
            '''
        flash('Usuário ou senha incorretos.')
    return render_template('login.html', form=form, header='Entrar')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você foi desconectado')
    return redirect(url_for('index'))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404