'''
livraria/__init__.py

Inicialização do pacote livraria, executado na importação.
'''

from flask import Flask
from flask_bootstrap import Bootstrap
from config import config

def set_config(ambiente):
    '''Sobrescreve as configurações base conforme o ambiente'''
    app.config.from_object(config[ambiente])
    bootstrap = Bootstrap(app)
    from .models import db
    db.init_app(app)

app = Flask(__name__)
app.config.from_object(config['base'])
from .views import *
