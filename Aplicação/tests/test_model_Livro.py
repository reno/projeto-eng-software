import unittest
from test_model import TesteModels
from livraria.models import db, Livro

dados_livro = {'titulo':'livro', 'autor':'autor', 'editora':'editora',
               'edicao':1, 'ano':'2019', 'isbn':'1', 'idioma':'Pt',
               'preco':9.99, 'exemplares':1}

class TesteLivro(TesteModels):

    def teste_consulta(self):
        livro = Livro(**dados_livro)
        db.session.add(livro)
        db.session.commit()
        consulta = Livro.query.get(1)
        self.assertIsInstance(consulta, Livro)

    def teste_cadastro(self):
        livro = Livro(**dados_livro)
        db.session.add(livro)
        db.session.commit()
        self.assertTrue(livro in db.session) 

    def teste_atualizacao(self):
        livro = Livro(**dados_livro)
        db.session.add(livro)
        livro.quantidade = 2
        db.session.commit()
        confirmacao = Livro.query.get(1)
        self.assertEqual(livro.quantidade, confirmacao.quantidade)

    def teste_exclusao(self):
        livro = Livro(**dados_livro)
        db.session.add(livro)
        db.session.commit()
        livro = Livro.query.get(1)
        db.session.delete(livro)
        db.session.commit()
        self.assertFalse(livro in db.session)
