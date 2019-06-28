"""
livraria/tables.py

Define tabelas usadas no resultado das consultas.
"""

from flask_table import Table, Col, DateCol, NestedTableCol
from isbnlib import mask


class IsbnCol(Col):
    """Customização do campo de ISBN."""
    def td_format(self, content):
        try:
            return mask(content)
        except:
            return content


class TitleCol(Col):
    """Customização do campo de título."""
    def td_format(self, content):
        return f'{content.titulo}'


class PriceCol(Col):
    """Customização do campo de preço."""
    def td_format(self, content):
        try:
            return f'R$ {content:5.2f}'
        except:
            return content

class PercentCol(Col):
    """Customização do campo de desconto."""
    def td_format(self, content):
        try:
            return f'{content}%'
        except:
            return content

class EditionCol(Col):
    """Customização do campo de edição."""
    def td_format(self, content):
        return f'{content}ª'

class ActiveCol(Col):
    """Customização do campo ativo do pedido."""
    def td_format(self, content):
        if content is True:
            return 'Ativo'
        else:
            return 'Cancelado'


class TabelaLivros(Table):
    """Tabela para exibição de resultados de consultas de Livros."""
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
    """Tabela para exibição de resultados de consultas de Clientes."""
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
    """Tabela para exibição de resultados de consultas de Funcionarios."""
    classes = ['table', 'table-striped', 'col-lg-3']
    no_items = 'Nenhum vendedor encontrado.'
    id = Col('Registro')
    nome = Col('Nome')
    usuario = Col('Usuário')

    
class TabelaItens(Table):
    """Subtabela de Pedidos"""
    livro = TitleCol('Livro')
    quantidade = Col('Qnt.')

class TabelaPedidos(Table):
    """Tabela para exibição de resultados de consultas de Pedidos."""
    classes = ['table', 'table-striped', 'col-lg-3']
    no_items = 'Nenhum pedido encontrado.'
    id = Col('Nº pedido')
    cliente = Col('Cliente')
    vendedor = Col('Vendedor')
    itens = NestedTableCol('Itens', TabelaItens)
    desconto = PercentCol('Desconto')
    total = PriceCol('Total')
    ativo = ActiveCol('Status')
