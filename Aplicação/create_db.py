'''
create_db.py

Script para criação do banco de dados. Recebe argumento ('dev', 'testes' ou 'producao').
'''

from sys import argv
from flask import Flask
from config import config
from livraria.models import *

app = Flask(__name__)
app.config.from_object(config[argv[1] or 'dev'])
db.init_app(app)  # inicializado em models.py 

def main():
    db.drop_all()
    db.create_all()
    admin = Funcionario(nome='Administrador', usuario='admin', senha='admin', admin=True)
    vendedor = Vendedor(nome='Vendedor', usuario='vendedor', senha='1234')
    endereco = Endereco(logradouro='rua', numero='sn', bairro='bairro',
                        cidade='Lavras', estado='MG', cep= '37200000')
    cliente = Cliente(nome='Cliente', documento='12345678', data_nascimento='01/01/1990',
                      endereco=endereco, telefone='3598765432', email='cliente@dominio.com')
    livro = Livro(titulo='livro', autor='autor', editora='editora', edicao=1,
                  ano='2019', isbn='1', idioma='Pt', preco=9.99, exemplares=10)
    db.session.add(admin)
    db.session.add(vendedor)
    db.session.add(cliente)
    db.session.add(livro)
    db.session.commit()
    print('BD criado com sucesso.')


if __name__ == "__main__":
    with app.app_context():
        main()
