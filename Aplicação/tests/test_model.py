"""
tests/test_model.py

Classe base dos testes unitários.
"""

from flask_testing import TestCase
from livraria import app
from livraria.models import db

class TesteModels(TestCase):

    def create_app(self):
        """Executado na inicialização"""
        return app

    def setUp(self):
        """Método chamado antes do início de cada teste"""
        db.drop_all()
        db.create_all()

    def tearDown(self):
        """Método chamado ao término de cada teste"""
        db.session.remove()
        db.drop_all()