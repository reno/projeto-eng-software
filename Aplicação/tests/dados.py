
livro = {
    'titulo':'livro',
    'autor':'autor',
    'editora':'editora',
    'edicao':1,
    'ano':'2019',
    'isbn':'1',
    'idioma':'Pt',
    'preco':'9.99',
    'exemplares':1
}

endereco = {
    'logradouro':'Av Bueno da Fonseca',
    'numero':'296',
    'bairro':'Centro',
    'cidade':'Lavras',
    'estado':'MG',
    'cep': '37200000'
}

cliente = {
    'nome': 'José da Silva',
    'documento': '12345678',
    'data_nascimento': '01/01/1990',
    'telefone': '3598765432',
    'email': 'jose@silva.com'
}

vendedor = {
    'nome': 'Vendedor',
    'usuario': 'vendedor',
    'senha': 'vendedor',
    'admin': False
}

vendedor_2 = {
    'nome': 'Gabriel',
    'usuario': 'gabriel',
    'senha': 'gabriel',
    'admin': False
}

admin = {
    'nome':'Administrador',
    'usuario': 'admin',
    'senha': 'admin',
    'admin': True
}

pedido = {
    'cliente': cliente['documento'],
    'livro': livro['isbn'],
    'quantidade': 1,
    'desconto': 0
}
