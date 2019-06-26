import unittest
from test_model import TesteModels
from livraria.models import db, Cliente, Endereco

dados_endereco = {
    'logradouro':'rua', 'numero':'sn', 'bairro':'bairro',
    'cidade':'Lavras', 'estado':'MG', 'cep': '37200000'
}

dados_cliente = {
    'nome':'Cliente', 'documento':'12345678', 'data_nascimento':'01/01/1990',
    'telefone':'3598765432', 'email':'cliente@dominio.com'
}

class TesteCliente(TesteModels):

    def teste_consulta(self):
        cliente = Cliente(**dados_cliente)
        endereco = Endereco(**dados_endereco)
        cliente.endereco = endereco
        db.session.add(cliente)
        db.session.commit()
        consulta = Cliente.query.get(1)
        self.assertIsInstance(consulta, Cliente)

    def teste_cadastro(self):
        cliente = Cliente(**dados_cliente)
        endereco = Endereco(**dados_endereco)
        cliente.endereco = endereco
        db.session.add(cliente)
        db.session.commit()
        self.assertTrue(cliente in db.session) 

    def teste_atualizacao(self):
        cliente = Cliente(**dados_cliente)
        endereco = Endereco(**dados_endereco)
        cliente.endereco = endereco
        db.session.add(cliente)
        cliente.quantidade = 2
        db.session.commit()
        confirmacao = Cliente.query.get(1)
        self.assertEqual(cliente.quantidade, confirmacao.quantidade)

    def teste_exclusao(self):
        cliente = Cliente(**dados_cliente)
        endereco = Endereco(**dados_endereco)
        cliente.endereco = endereco
        db.session.add(cliente)
        db.session.commit()
        cliente = Cliente.query.get(1)
        db.session.delete(cliente)
        db.session.commit()
        self.assertFalse(cliente in db.session)
