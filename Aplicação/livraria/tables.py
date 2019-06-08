'''
livraria/tables.py

Define tabelas usadas no resultado das consultas.
'''

from flask_table import Table, Col

class TabelaLivros(Table):
    id = Col('ID', show=False)
    isbn = Col('ISBN')
    titulo = Col('Título')
    autor = Col('Autor')
    editora = Col('Editora')
    edicao = Col('Edição')
    ano = Col('Ano')
    preco = Col('Preço')
    exemplares = Col('Exemplares')