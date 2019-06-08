'''
config.py

Define configurações para diferentes ambientes.
'''

import os

basedir = os.path.abspath(os.path.dirname(__file__))
SQLLITE = 'sqlite:///' + os.path.join(basedir, 'livraria.db')
POSTGRE = 'postgres://localhost/livraria'

class Config:
    SECRET_KEY = 'string de verificacao do flask-wtf'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = POSTGRE

class ConfigDesenvolvimento(Config):
    SERVER_NAME = 'localhost:5000'
    DEBUG = True

class ConfigTestes(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or POSTGRE

class ConfigProducao(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or POSTGRE
    SECRET_KEY = os.environ.get('SECRET_KEY')

config = {
    'base': Config,
    'dev': ConfigDesenvolvimento,
    'testes': ConfigTestes,
    'producao': ConfigProducao
}