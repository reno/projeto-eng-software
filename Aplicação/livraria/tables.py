'''
livraria/tables.py

Define tabelas usadas no resultado das consultas.
'''

from flask_table import Table, Col
from isbnlib import mask

class IsbnCol(Col):
    def td_format(self, content):
        try:
            return mask(content)
        except:
            return content


class PriceCol(Col):
    def td_format(self, content):
        return 'R$ {:5.2f}'.format(content)


class EditionCol(Col):
    def td_format(self, content):
        return '{}ª'.format(content)


class TabelaLivros(Table):
    classes = ['table', 'table-striped', 'col-lg-3']
    id = Col('ID', show=False)
    isbn = IsbnCol('ISBN')
    titulo = Col('Título')
    autor = Col('Autor')
    editora = Col('Editora')
    edicao = EditionCol('Edição')
    ano = Col('Ano')
    preco = PriceCol('Preço')
    exemplares = Col('Exemplares')