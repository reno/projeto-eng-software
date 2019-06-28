"""
decorators.py

Implementa o padrão de projeto Decorator, descrito no livro
Design Patterns, da "Gang of Four". 

Decorators são padrões estruturais que permitem adicionar comportamentos
a um objeto individual, sem afetar os demais objetos da classe. 

A implementação em python é feita com auxílio da função wraps, disponível
no módulo functools. Para aplicar um decorator basta incluir @decorator
na linha anterior a um objeto (em python, funções também são objetos). 

O decorator abaixo faz com que uma função seja acessível apenas 
por usuários com permissão de administrador. Ele será necessário
no controle das rotas do menu admin (livraria/views/admin.py)

O framework Flask também faz uso extensivo de decorators, como pode ser
verificado nos demais arquivos da pasta livraria/views.
"""

from functools import wraps
from flask import abort
from flask_login import current_user
from .models import Funcionario

def admin():
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_admin():
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def admin_required(f):
    """Restringe o acesso de uma função a usuários administradores."""
    return admin()(f)
