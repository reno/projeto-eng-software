from flask_testing import TestCase
from livraria import app
from livraria.models import db

class TesteModels(TestCase):

    def create_app(self):
        return app

    def setUp(self):
        db.drop_all()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()