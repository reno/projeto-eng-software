'''
app.py

Instancia app, para desenvolvimento. Recebe argumento ('dev', 'testes' ou 'producao').
'''

from sys import argv
import livraria
if argv[1]: livraria.set_config(argv[1])
from livraria import app

if __name__ == '__main__':
    app.run(debug=True)