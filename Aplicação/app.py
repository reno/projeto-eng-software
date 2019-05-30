from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from models import *

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost/livraria'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app = Flask(__name__)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
db.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
