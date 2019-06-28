"""
livraria/__init__.py

Inicialização do pacote livraria, executado na importação.
"""

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from config import config

def set_config(ambiente):
    """Sobrescreve as configurações base conforme o ambiente"""
    app.config.from_object(config[ambiente])

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message = 'Entre com seu usuário para acessar esta página.'

# executado na importação:
app = Flask(__name__)
app.config.from_object(config['base'])
from .views import principal, livro, pedido, cliente, admin

app.config['WTF_CSRF_SECRET_KEY'] = 'string de verificacao do flask-wtf'

csrf = CSRFProtect(app)
login_manager.init_app(app)
bootstrap = Bootstrap(app)

from .models import db
db.init_app(app)


