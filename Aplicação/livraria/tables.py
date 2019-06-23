'''
livraria/tables.py

Define tabelas usadas no resultado das consultas.
'''

from flask_table import Table, Col, DateCol, NestedTableCol
from isbnlib import mask


class IsbnCol(Col):
    def td_format(self, content):
        try:
            return mask(content)
        except:
            return content


class TitleCol(Col):
    def td_format(self, content):
        return '{}'.format(content.titulo) 


class PriceCol(Col):
    def td_format(self, content):
        return 'R$ {:5.2f}'.format(content)


class EditionCol(Col):
    def td_format(self, content):
        return '{}ª'.format(content)

class ActiveCol(Col):
    def td_format(self, content):
        if content is True:
            return 'Ativo'
        else:
            return 'Cancelado'



class TabelaLivros(Table):
    classes = ['table', 'table-striped', 'col-lg-3']
    no_items = 'Nenhum livro encontrado.'
    id = Col('ID', show=False)
    isbn = IsbnCol('ISBN')
    titulo = Col('Título')
    autor = Col('Autor')
    editora = Col('Editora')
    edicao = EditionCol('Edição')
    ano = Col('Ano')
    preco = PriceCol('Preço')
    exemplares = Col('Exemplares')


class TabelaClientes(Table):
    classes = ['table', 'table-striped', 'col-lg-3']
    no_items = 'Nenhum cliente encontrado.'
    id = Col('ID', show=False)
    nome = Col('Nome')
    documento = Col('Documento')
    data_nascimento = DateCol('Data de nasc.')
    endereco = Col('Endereço')
    telefone = Col('Telefone')
    email = Col('E-mail')


class TabelaFuncionarios(Table):
    classes = ['table', 'table-striped', 'col-lg-3']
    no_items = 'Nenhum funcionário encontrado.'
    id = Col('Registro')
    nome = Col('Nome')
    usuario = Col('Usuário')

    
class TabelaItens(Table):
    livro = TitleCol('Livro')
    quantidade = Col('Qnt.')

class TabelaPedidos(Table):
    classes = ['table', 'table-striped', 'col-lg-3']
    no_items = 'Nenhum pedido encontrado.'
    id = Col('Nº pedido')
    cliente = Col('Cliente')
    vendedor = Col('Vendedor')
    itens = NestedTableCol('Itens', TabelaItens)
    desconto = PriceCol('Desconto')
    total = PriceCol('Total')
    ativo = ActiveCol('Status')
