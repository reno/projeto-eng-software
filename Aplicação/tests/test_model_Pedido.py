"""
tests/test_model_Pedido.py

Testes unitários das operações sobre a tabela Pedidos
"""

from test_model import TesteModels
from livraria.models import *
import tests.dados as dados


class TestePedido(TesteModels):

    def teste_consulta(self):
        livro = Livro(**dados.livro)
        cliente = Cliente(**dados.cliente)
        endereco = Endereco(**dados.endereco)
        cliente.endereco = endereco
        vendedor = Funcionario(**dados.vendedor)
        item = ItemPedido(livro=livro, quantidade=1)
        pedido = Pedido(cliente=cliente, vendedor=vendedor, desconto=0)
        pedido.itens.append(item)
        db.session.add(pedido)
        db.session.commit()
        consulta = Pedido.query.get(1)
        self.assertIsInstance(consulta, Pedido)

    def teste_cadastro(self):
        livro = Livro(**dados.livro)
        cliente = Cliente(**dados.cliente)
        endereco = Endereco(**dados.endereco)
        cliente.endereco = endereco
        vendedor = Funcionario(**dados.vendedor)
        item = ItemPedido(livro=livro, quantidade=1)
        pedido = Pedido(cliente=cliente, vendedor=vendedor, desconto=0)
        pedido.itens.append(item)
        db.session.add(pedido)
        db.session.commit()
        self.assertTrue(pedido in db.session)

    def teste_atualizacao(self):
        livro = Livro(**dados.livro)
        cliente = Cliente(**dados.cliente)
        endereco = Endereco(**dados.endereco)
        cliente.endereco = endereco
        vendedor = Funcionario(**dados.vendedor)
        item = ItemPedido(livro=livro, quantidade=1)
        pedido = Pedido(cliente=cliente, vendedor=vendedor, desconto=0, total=0)
        pedido.itens.append(item)
        db.session.add(pedido)
        db.session.commit()
        atualizacao = Pedido.query.get(1)
        db.session.add(atualizacao)
        atualizacao.desconto = 10
        db.session.commit()
        confirmacao = Pedido.query.get(1).itens
        self.assertNotEqual(confirmacao, pedido)

    def teste_exclusao(self):
        livro = Livro(**dados.livro)
        cliente = Cliente(**dados.cliente)
        endereco = Endereco(**dados.endereco)
        cliente.endereco = endereco
        vendedor = Funcionario(**dados.vendedor)
        item = ItemPedido(livro=livro, quantidade=1)
        pedido = Pedido(cliente=cliente, vendedor=vendedor, desconto=0)
        pedido.itens.append(item)
        db.session.add(pedido)
        db.session.commit()
        pedido = Pedido.query.get(1)
        pedido.ativo = False
        db.session.commit()
        confirmacao = Pedido.query.get(1)
        self.assertFalse(confirmacao.ativo)
