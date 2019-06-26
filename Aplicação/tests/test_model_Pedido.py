import unittest
from test_model import TesteModels
from livraria.models import db, Livro, Funcionario, Cliente, Endereco,\
                            ItemPedido, Pedido

dados_livro = {'titulo':'livro', 'autor':'autor', 'editora':'editora',
               'edicao':1, 'ano':'2019', 'isbn':'1', 'idioma':'Pt',
               'preco':9.99, 'exemplares':1}

dados_funcionario = {'nome':'Vendedor', 'usuario':'vendedor', 'senha':'vendedor'}

dados_endereco = {
    'logradouro':'rua', 'numero':'sn', 'bairro':'bairro',
    'cidade':'Lavras', 'estado':'MG', 'cep': '37200000'
}

dados_cliente = {
    'nome':'Pedido', 'documento':'12345678', 'data_nascimento':'01/01/1990',
    'telefone':'3598765432', 'email':'pedido@dominio.com'
}


class TestePedido(TesteModels):

    def teste_consulta(self):
        livro = Livro(**dados_livro)
        cliente = Cliente(**dados_cliente)
        endereco = Endereco(**dados_endereco)
        cliente.endereco = endereco
        vendedor = Funcionario(**dados_funcionario)
        item = ItemPedido(livro=livro, quantidade=1)
        pedido = Pedido(cliente=cliente, vendedor=vendedor, desconto=0)
        db.session.add(pedido)
        db.session.commit()
        consulta = Pedido.query.get(1)
        self.assertIsInstance(consulta, Pedido)

    def teste_cadastro(self):
        livro = Livro(**dados_livro)
        cliente = Cliente(**dados_cliente)
        endereco = Endereco(**dados_endereco)
        cliente.endereco = endereco
        vendedor = Funcionario(**dados_funcionario)
        item = ItemPedido(livro=livro, quantidade=1)
        pedido = Pedido(cliente=cliente, vendedor=vendedor, desconto=0)
        pedido.itens.append(item)
        db.session.add(pedido)
        db.session.commit()
        self.assertTrue(pedido in db.session) 

    def teste_atualizacao(self):
        livro = Livro(**dados_livro)
        cliente = Cliente(**dados_cliente)
        endereco = Endereco(**dados_endereco)
        cliente.endereco = endereco
        vendedor = Funcionario(**dados_funcionario)
        item = ItemPedido(livro=livro, quantidade=1)
        pedido = Pedido(cliente=cliente, vendedor=vendedor, desconto=0)
        pedido.itens.append(item)
        db.session.add(pedido)
        pedido.itens.quantidade = 2
        db.session.commit()
        confirmacao = ItemPedido.query.get(1)
        self.assertEqual(confirmacao.quantidade, 2)

    def teste_exclusao(self):
        livro = Livro(**dados_livro)
        cliente = Cliente(**dados_cliente)
        endereco = Endereco(**dados_endereco)
        cliente.endereco = endereco
        vendedor = Funcionario(**dados_funcionario)
        item = ItemPedido(livro=livro, quantidade=1)
        pedido = Pedido(cliente=cliente, vendedor=vendedor, desconto=0)
        pedido.itens.append(item)
        db.session.add(pedido)
        db.session.commit()
        pedido = Pedido.query.get(1)
        pedido.ativo = False
        #db.session.delete(pedido)
        db.session.commit()
        confirmacao = Pedido.query.get(1)
        self.assertFalse(confirmacao.ativo)
