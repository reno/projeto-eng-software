'''
livraria/__init__.py

Inicialização do pacote livraria, executado na importação.
'''

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from config import config

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message = 'Entre com seu usuário para acessar esta página.'

def set_config(ambiente):
    '''Sobrescreve as configurações base conforme o ambiente'''
    app.config.from_object(config[ambiente])
    bootstrap = Bootstrap(app)
    from .models import db
    db.init_app(app)
    login_manager.init_app(app)

# executado na importação:
app = Flask(__name__)
app.config.from_object(config['base'])
from .views import principal, livro
