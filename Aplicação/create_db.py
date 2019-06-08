'''
create_db.py

Script para criação do banco de dados. Recebe argumento ('dev', 'testes' ou 'producao').
'''

from sys import argv
from flask import Flask
from config import config
from livraria.models import *

app = Flask(__name__)
app.config.from_object(config[argv[1] or 'dev'])
db.init_app(app)  # inicializado em models.py 

def main():
    db.create_all()
    print('BD criado com sucesso.')

if __name__ == "__main__":
    with app.app_context():
        main()
