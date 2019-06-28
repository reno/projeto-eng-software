"""
tests/test_model_Cliente.py

Testes unitários das operações sobre a tabela Clientes
"""

from test_model import TesteModels
from livraria.models import db, Cliente, Endereco
import tests.dados as dados


class TesteCliente(TesteModels):

    def teste_consulta(self):
        cliente = Cliente(**dados.cliente)
        endereco = Endereco(**dados.endereco)
        cliente.endereco = endereco
        db.session.add(cliente)
        db.session.commit()
        consulta = Cliente.query.get(1)
        self.assertIsInstance(consulta, Cliente)

    def teste_cadastro(self):
        cliente = Cliente(**dados.cliente)
        endereco = Endereco(**dados.endereco)
        cliente.endereco = endereco
        db.session.add(cliente)
        db.session.commit()
        self.assertTrue(cliente in db.session) 

    def teste_atualizacao(self):
        cliente = Cliente(**dados.cliente)
        endereco = Endereco(**dados.endereco)
        cliente.endereco = endereco
        db.session.add(cliente)
        cliente.quantidade = 2
        db.session.commit()
        confirmacao = Cliente.query.get(1)
        self.assertEqual(cliente.quantidade, confirmacao.quantidade)

    def teste_exclusao(self):
        cliente = Cliente(**dados.cliente)
        endereco = Endereco(**dados.endereco)
        cliente.endereco = endereco
        db.session.add(cliente)
        db.session.commit()
        cliente = Cliente.query.get(1)
        db.session.delete(cliente)
        db.session.commit()
        self.assertFalse(cliente in db.session)
