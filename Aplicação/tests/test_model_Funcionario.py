import unittest
from livraria.models import Funcionario

class CasoTesteFuncionario(unittest.TestCase):
    def teste_set_senha(self):
        f = Funcionario(senha='teste')
        self.assertTrue(f.senha_hash is not None)

    def teste_get_senha(self):
        f = Funcionario(senha='teste')
        with self.assertRaises(AttributeError):
            f.senha

    def teste_verifica_senha(self):
        f = Funcionario(senha='teste')
        self.assertTrue(f.verifica_senha('teste'))
        self.assertFalse(f.verifica_senha('123'))

    def teste_random_salts(self):
        f1 = Funcionario(senha = 'teste')
        f2 = Funcionario(senha = 'teste')
        self.assertTrue(f1.senha_hash != f2.senha_hash)