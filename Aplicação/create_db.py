import os
from flask import Flask
from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost/livraria'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# db é inicializado em models.py 
db.init_app(app)

def main():
    db.create_all()
    print('BD criado com sucesso.')

if __name__ == "__main__":
    with app.app_context():
        main()
