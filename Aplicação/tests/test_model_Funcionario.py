"""
tests/test_model_Funcionario.py

Testes unitários das operações sobre a tabela Funcionarios
"""

from test_model import TesteModels
from livraria.models import db, Funcionario
import tests.dados as dados


class TesteFuncionario(TesteModels):

    def teste_consulta(self):
        funcionario = Funcionario(**dados.vendedor)
        db.session.add(funcionario)
        db.session.commit()
        consulta = Funcionario.query.get(1)
        self.assertIsInstance(consulta, Funcionario)

    def teste_cadastro(self):
        funcionario = Funcionario(**dados.vendedor)
        db.session.add(funcionario)
        db.session.commit()
        self.assertTrue(funcionario in db.session)

    def teste_atualizacao(self):
        funcionario = Funcionario(**dados.vendedor)
        db.session.add(funcionario)
        funcionario.quantidade = 2
        db.session.commit()
        confirmacao = Funcionario.query.get(1)
        self.assertEqual(funcionario.quantidade, confirmacao.quantidade)

    def teste_exclusao(self):
        funcionario = Funcionario(**dados.vendedor)
        db.session.add(funcionario)
        db.session.commit()
        funcionario = Funcionario.query.get(1)
        db.session.delete(funcionario)
        db.session.commit()
        self.assertFalse(funcionario in db.session)

    def teste_set_senha(self):
        funcionario = Funcionario(**dados.vendedor)
        self.assertTrue(funcionario.senha_hash is not None)

    def teste_get_senha(self):
        funcionario = Funcionario(**dados.vendedor)
        with self.assertRaises(AttributeError):
            funcionario.senha

    def teste_verifica_senha(self):
        funcionario = Funcionario(**dados.vendedor)
        self.assertTrue(funcionario.verifica_senha(dados.vendedor['senha']))
        self.assertFalse(funcionario.verifica_senha('123'))

    def teste_random_salts(self):
        f1 = Funcionario(nome='Teste1', usuario='teste1', senha='teste')
        f2 = Funcionario(nome='Teste2', usuario='teste2', senha='teste')
        self.assertTrue(f1.senha_hash != f2.senha_hash)