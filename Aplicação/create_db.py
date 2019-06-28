"""
create_db.py

Script para inicialização do banco de dados.
Também insere dados no BD para facilitar testes manuais no sistema.
"""

#from sys import argv
from flask import Flask
from config import config
from livraria.models import *
import tests.dados as dados

app = Flask(__name__)
app.config.from_object(config['dev'])
db.init_app(app)  # inicializado em models.py 


def main():
    db.drop_all()
    db.create_all()
    # Instancia e insere objetos no BD
    admin = Funcionario(**dados.admin)
    vendedor = Vendedor(**dados.vendedor)
    endereco = Endereco(**dados.endereco)
    cliente = Cliente(**dados.cliente)
    cliente.endereco = endereco
    livro = Livro(**dados.livro)
    item = ItemPedido(livro=livro, quantidade=1)
    pedido = Pedido(cliente=cliente, vendedor=vendedor, desconto=0)
    pedido.itens.append(item)
    db.session.add(admin)
    db.session.add(vendedor)
    db.session.add(cliente)
    db.session.add(livro)
    db.session.add(pedido)
    db.session.commit()
    # Fim das inserções
    print('BD criado com sucesso.')


if __name__ == "__main__":
    with app.app_context():
        main()
