"""
tests/test_model_Livro.py

Testes unitários das operações sobre a tabela Livro
"""

from test_model import TesteModels
from livraria.models import db, Livro
import tests.dados as dados


class TesteLivro(TesteModels):

    def teste_consulta(self):
        livro = Livro(**dados.livro)
        db.session.add(livro)
        db.session.commit()
        consulta = Livro.query.get(1)
        self.assertIsInstance(consulta, Livro)

    def teste_cadastro(self):
        livro = Livro(**dados.livro)
        db.session.add(livro)
        db.session.commit()
        self.assertTrue(livro in db.session) 

    def teste_atualizacao(self):
        livro = Livro(**dados.livro)
        db.session.add(livro)
        livro.quantidade = 2
        db.session.commit()
        confirmacao = Livro.query.get(1)
        self.assertEqual(livro.quantidade, confirmacao.quantidade)

    def teste_exclusao(self):
        livro = Livro(**dados.livro)
        db.session.add(livro)
        db.session.commit()
        livro = Livro.query.get(1)
        db.session.delete(livro)
        db.session.commit()
        self.assertFalse(livro in db.session)
