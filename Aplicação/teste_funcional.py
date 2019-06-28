"""
teste_funcional.py

Define e executa os testes funcionais.
Ao executar o arquivo, todos os métodos que iniciam com o nome
"test" serão executados.
"""

import unittest
import time
from flask import url_for
from flask_testing import TestCase, LiveServerTestCase
from urllib.request import urlopen
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from isbnlib import mask
import livraria
from livraria import app
from livraria.models import *
import tests.dados as dados

DELAY = 0.3

class TestBase(LiveServerTestCase):
    """Classe base dos testes funcionais"""

    def create_app(self):
        """Executa rotinas de inicialização dos testes"""
        livraria.set_config('testes')
        app.config.update(LIVESERVER_PORT=8943)
        return app

    def setUp(self):
        """Método chamado antes do início de cada teste"""
        self.driver = webdriver.Chrome()
        self.driver.get(self.get_server_url())
        db.drop_all()
        db.create_all()
        livro = Livro(**dados.livro)
        db.session.add(livro)
        cliente = Cliente(**dados.cliente)
        db.session.add(cliente)
        endereco = Endereco(**dados.endereco)
        cliente.endereco = endereco
        admin = Funcionario(**dados.admin)
        db.session.add(admin)
        vendedor = Funcionario(**dados.vendedor)
        db.session.add(vendedor)
        item = ItemPedido(livro=livro, quantidade=1)
        pedido = Pedido(cliente=cliente, vendedor=vendedor, desconto=0)
        pedido.itens.append(item)
        db.session.add(pedido)
        db.session.commit()

    def tearDown(self):
        """Método chamado ao término de cada teste"""
        self.driver.quit()
        db.session.remove()
        db.drop_all()

    def test_server_is_up(self):
        """Verifica se o servidor está ativo"""
        response = urlopen(self.get_server_url())
        self.assertEqual(response.code, 200)

    def login_admin(self):
        """Entra com o usuário administrador"""
        login_link = self.get_server_url() + url_for('login')
        self.driver.get(login_link)
        self.driver.find_element_by_id('usuario').send_keys(dados.admin['usuario'])
        self.driver.find_element_by_id('senha').send_keys(dados.admin['senha'])
        self.driver.find_element_by_id('submit').click()

    def login_vendedor(self):
        """Entra com o usuário comum""" 
        login_link = self.get_server_url() + url_for('login')
        self.driver.get(login_link)
        self.driver.find_element_by_id('usuario').send_keys(dados.vendedor['usuario'])
        self.driver.find_element_by_id('senha').send_keys(dados.vendedor['senha'])
        self.driver.find_element_by_id('submit').click()


class TestLogin(TestBase):
    """Define os testes de login"""

    def test_login(self):
        self.driver.find_element_by_id('usuario').send_keys(dados.admin['usuario'])
        self.driver.find_element_by_id('senha').send_keys(dados.admin['senha'])
        self.driver.find_element_by_id('submit').click()
        time.sleep(1)
        assert url_for('index') in self.driver.current_url

    def test_login_admin(self):
        self.driver.find_element_by_id('usuario').send_keys(dados.admin['usuario'])
        self.driver.find_element_by_id('senha').send_keys(dados.admin['senha'])
        self.driver.find_element_by_id('submit').click()
        time.sleep(1)
        assert url_for('index') in self.driver.current_url

    def test_login_usuario_incorreto(self):
        self.driver.find_element_by_id('usuario').send_keys('incorreto')
        self.driver.find_element_by_id('senha').send_keys(dados.vendedor['senha'])
        self.driver.find_element_by_id('submit').click()
        time.sleep(DELAY)
        alerta = self.driver.find_element_by_class_name('alert').text
        assert 'Usuário ou senha incorretos.' in alerta

    def test_login_senha_incorreta(self):
        self.driver.find_element_by_id('usuario').send_keys(dados.vendedor['usuario'])
        self.driver.find_element_by_id('senha').send_keys('incorreta')
        self.driver.find_element_by_id('submit').click()
        time.sleep(DELAY)
        alerta = self.driver.find_element_by_class_name('alert').text
        assert 'Usuário ou senha incorretos.' in alerta


class TestLivros(TestBase):
    """Define os testes do menu Livros"""

    def test_consultar(self):
        self.login_vendedor()
        time.sleep(DELAY)
        self.driver.find_element_by_id('menuLivros').click()
        time.sleep(DELAY)
        self.driver.find_element_by_id('consultarLivro').click()
        time.sleep(DELAY)
        self.driver.find_element_by_id('campo').send_keys('titulo')
        titulo = dados.livro['titulo']
        self.driver.find_element_by_id('termo').send_keys(titulo)
        self.driver.find_element_by_id('submit').click()
        time.sleep(DELAY)
        tabela_obj = self.driver.find_elements_by_tag_name('td')
        tabela = [linha.text for linha in tabela_obj]
        assert dados.livro['titulo'] in tabela


    def test_consultar_inexistente(self):
        self.login_vendedor()
        time.sleep(DELAY)
        self.driver.find_element_by_id('menuLivros').click()
        time.sleep(DELAY)
        self.driver.find_element_by_id('consultarLivro').click()
        time.sleep(DELAY)
        self.driver.find_element_by_id('campo').send_keys('titulo')
        self.driver.find_element_by_id('termo').send_keys('inexistente')
        self.driver.find_element_by_id('submit').click()
        time.sleep(DELAY)
        texto = self.driver.find_element_by_tag_name('p').text
        assert 'Nenhum livro encontrado.' in texto

    def _cadastrar(self):
        self.driver.find_element_by_id('menuLivros').click()
        time.sleep(DELAY)
        self.driver.find_element_by_id('cadastrarLivro').click()
        time.sleep(DELAY)
        self.driver.find_element_by_id('titulo').send_keys(dados.livro['titulo'])
        self.driver.find_element_by_id('autor').send_keys(dados.livro['autor'])
        self.driver.find_element_by_id('editora').send_keys(dados.livro['editora'])
        self.driver.find_element_by_id('edicao').send_keys(dados.livro['edicao'])
        self.driver.find_element_by_id('ano').send_keys(dados.livro['ano'])
        self.driver.find_element_by_id('isbn_field').send_keys(dados.livro['isbn'])
        self.driver.find_element_by_id('idioma').send_keys(dados.livro['idioma'])
        self.driver.find_element_by_id('preco').send_keys(dados.livro['preco'])
        self.driver.find_element_by_id('exemplares').send_keys(dados.livro['exemplares'])
        self.driver.find_element_by_id('submit').click()
        time.sleep(DELAY)

    def test_cadastrar(self):
        self.login_vendedor()
        time.sleep(DELAY)
        self._cadastrar()
        confirmacao = self.driver.find_element_by_tag_name('p').text
        assert dados.livro['isbn'] in confirmacao # usar mask?

    def test_cadastrar_existente(self):
        self.login_vendedor()
        time.sleep(DELAY)
        self._cadastrar()
        self._cadastrar()
        erro = self.driver.find_element_by_tag_name('p').text
        assert 'já cadastrado' in erro

    def test_atualizar(self):
        self.login_vendedor()
        time.sleep(DELAY)
        self.driver.find_element_by_id('menuLivros').click()
        time.sleep(DELAY)
        self.driver.find_element_by_id('atualizarLivro').click()
        time.sleep(DELAY)
        self.driver.find_element_by_id('isbn').send_keys(dados.livro['isbn'])
        self.driver.find_element_by_id('submit').click()
        time.sleep(DELAY)
        campo_exemplares = self.driver.find_element_by_id('exemplares')
        for i in range(10):
            campo_exemplares.send_keys(Keys.BACKSPACE)
        exemplares = dados.livro['exemplares'] * 2
        self.driver.find_element_by_id('exemplares').send_keys(exemplares)
        self.driver.find_element_by_id('submit').click()
        time.sleep(DELAY)
        confirmacao = self.driver.find_element_by_tag_name('p').text
        assert 'Livro atualizado com sucesso.' in confirmacao

    def test_atualizar_inexistente(self):
        self.login_vendedor()
        time.sleep(DELAY)
        self.driver.find_element_by_id('menuLivros').click()
        time.sleep(DELAY)
        self.driver.find_element_by_id('atualizarLivro').click()
        time.sleep(DELAY)
        self.driver.find_element_by_id('isbn').send_keys('1234567890')
        self.driver.find_element_by_id('submit').click()
        time.sleep(DELAY)
        erro = self.driver.find_element_by_tag_name('p').text
        assert 'Nenhum livro encontrado.' in erro

    def test_excluir(self):
        self.login_vendedor()
        time.sleep(DELAY)
        self.driver.find_element_by_id('menuLivros').click()
        time.sleep(DELAY)
        self.driver.find_element_by_id('excluirLivro').click()
        time.sleep(DELAY)
        self.driver.find_element_by_id('isbn').send_keys(dados.livro['isbn'])
        self.driver.find_element_by_id('submit').click()
        time.sleep(DELAY)
        tabela_obj = self.driver.find_elements_by_tag_name('td')
        tabela = [linha.text for linha in tabela_obj]
        assert dados.livro['titulo'] in tabela
        self.driver.find_element_by_id('submit').click()
        time.sleep(DELAY)
        confirmacao = self.driver.find_element_by_tag_name('p').text
        assert 'Livro excluido com sucesso.' in confirmacao


    def test_excluir_inexistente(self):
        self.login_vendedor()
        time.sleep(DELAY)
        self.driver.find_element_by_id('menuLivros').click()
        time.sleep(DELAY)
        self.driver.find_element_by_id('excluirLivro').click()
        time.sleep(DELAY)
        self.driver.find_element_by_id('isbn').send_keys('1234567890')
        self.driver.find_element_by_id('submit').click()
        time.sleep(DELAY)
        erro = self.driver.find_element_by_tag_name('p').text
        assert 'Nenhum livro encontrado.' in erro


class TestPedidos(TestBase):
    """Define os testes do menu Pedidos"""

    def test_consultar(self):
        self.login_vendedor()
        time.sleep(DELAY)
        self.driver.find_element_by_id('menuPedidos').click()
        time.sleep(DELAY)
        self.driver.find_element_by_id('consultarPedido').click()
        time.sleep(DELAY)
        self.driver.find_element_by_id('campo').send_keys('n')
        self.driver.find_element_by_id('termo').send_keys('1')
        self.driver.find_element_by_id('submit').click()
        time.sleep(DELAY)
        tabela_obj = self.driver.find_elements_by_tag_name('td')
        tabela = [linha.text for linha in tabela_obj]
        assert dados.pedido['cliente'] in tabela

    def test_consultar_inexistente(self):
        self.login_vendedor()
        time.sleep(DELAY)
        self.driver.find_element_by_id('menuPedidos').click()
        time.sleep(DELAY)
        self.driver.find_element_by_id('consultarPedido').click()
        time.sleep(DELAY)
        self.driver.find_element_by_id('termo').send_keys('99')
        self.driver.find_element_by_id('submit').click()
        time.sleep(DELAY)
        texto = self.driver.find_element_by_tag_name('p').text
        assert 'Nenhum pedido encontrado.' in texto

    def _cadastrar(self):
        self.driver.find_element_by_id('menuPedidos').click()
        time.sleep(DELAY)
        self.driver.find_element_by_id('cadastrarPedido').click()
        time.sleep(DELAY)
        self.driver.find_element_by_id('cliente').send_keys(dados.pedido['cliente'])
        self.driver.find_element_by_id('itens-0-livro').send_keys(dados.pedido['livro'])
        self.driver.find_element_by_id('itens-0-quantidade').send_keys(dados.pedido['quantidade'])
        self.driver.find_element_by_id('desconto').send_keys(dados.pedido['desconto'])
        self.driver.find_element_by_id('submit').click()
        time.sleep(DELAY)

    def test_cadastrar(self):
        self.login_vendedor()
        time.sleep(DELAY)
        self._cadastrar()
        confirmacao = self.driver.find_element_by_tag_name('p').text
        assert 'cadastrado com sucesso' in confirmacao

    def test_atualizar(self):
        self.login_vendedor()
        time.sleep(DELAY)
        self.driver.find_element_by_id('menuPedidos').click()
        time.sleep(DELAY)
        self.driver.find_element_by_id('atualizarPedido').click()
        time.sleep(DELAY)
        self.driver.find_element_by_id('pedido').send_keys(1)
        self.driver.find_element_by_id('submit').click()
        time.sleep(DELAY)
        campo_desconto = self.driver.find_element_by_id('desconto')
        for i in range(5):
            campo_desconto.send_keys(Keys.BACKSPACE)
        campo_desconto.send_keys('10')
        self.driver.find_element_by_id('submit').click()
        time.sleep(DELAY)
        confirmacao = self.driver.find_element_by_tag_name('p').text
        assert 'Pedido atualizado com sucesso.' in confirmacao

    def test_atualizar_inexistente(self):
        self.login_vendedor()
        time.sleep(DELAY)
        self.driver.find_element_by_id('menuPedidos').click()
        time.sleep(DELAY)
        self.driver.find_element_by_id('atualizarPedido').click()
        time.sleep(DELAY)
        self.driver.find_element_by_id('pedido').send_keys('9')
        self.driver.find_element_by_id('submit').click()
        time.sleep(DELAY)
        erro = self.driver.find_element_by_tag_name('p').text
        assert 'Nenhum pedido encontrado.' in erro

    def test_excluir(self):
        self.login_vendedor()
        time.sleep(DELAY)
        self.driver.find_element_by_id('menuPedidos').click()
        time.sleep(DELAY)
        self.driver.find_element_by_id('excluirPedido').click()
        time.sleep(DELAY)
        self.driver.find_element_by_id('pedido').send_keys(1)
        self.driver.find_element_by_id('submit').click()
        time.sleep(DELAY)
        tabela_obj = self.driver.find_elements_by_tag_name('td')
        tabela = [linha.text for linha in tabela_obj]
        assert dados.pedido['cliente'] in tabela
        self.driver.find_element_by_id('submit').click()
        time.sleep(DELAY)
        confirmacao = self.driver.find_element_by_tag_name('p').text
        assert 'cancelado com sucesso.' in confirmacao

    def test_excluir_inexistente(self):
        self.login_vendedor()
        time.sleep(DELAY)
        self.driver.find_element_by_id('menuPedidos').click()
        time.sleep(DELAY)
        self.driver.find_element_by_id('excluirPedido').click()
        time.sleep(DELAY)
        self.driver.find_element_by_id('pedido').send_keys('9')
        self.driver.find_element_by_id('submit').click()
        time.sleep(DELAY)
        erro = self.driver.find_element_by_tag_name('p').text
        assert 'Nenhum pedido encontrado.' in erro


class TestClientes(TestBase):
    """Define os testes do menu Clientes"""

    def test_consultar(self):
        self.login_vendedor()
        time.sleep(DELAY)
        self.driver.find_element_by_id('menuClientes').click()
        time.sleep(DELAY)
        self.driver.find_element_by_id('consultarCliente').click()
        time.sleep(DELAY)
        self.driver.find_element_by_id('campo').send_keys('documento')
        self.driver.find_element_by_id('termo').send_keys(dados.cliente['documento'])
        self.driver.find_element_by_id('submit').click()
        time.sleep(DELAY)
        tabela_obj = self.driver.find_elements_by_tag_name('td')
        tabela = [linha.text for linha in tabela_obj]
        assert dados.cliente['documento'] in tabela

    def test_consultar_inexistente(self):
        self.login_vendedor()
        time.sleep(DELAY)
        self.driver.find_element_by_id('menuClientes').click()
        time.sleep(DELAY)
        self.driver.find_element_by_id('consultarCliente').click()
        time.sleep(DELAY)
        self.driver.find_element_by_id('campo').send_keys('documento')
        self.driver.find_element_by_id('termo').send_keys('00000000')
        self.driver.find_element_by_id('submit').click()
        time.sleep(DELAY)
        erro = self.driver.find_element_by_tag_name('p').text
        assert 'Nenhum cliente encontrado.' in erro


    def _cadastrar(self):
        self.driver.find_element_by_id('menuClientes').click()
        time.sleep(DELAY)
        self.driver.find_element_by_id('cadastrarCliente').click()
        time.sleep(DELAY)
        self.driver.find_element_by_id('nome').send_keys(dados.cliente['nome'])
        self.driver.find_element_by_id('documento').send_keys(dados.cliente['documento'])
        self.driver.find_element_by_id('data_nascimento').send_keys(dados.cliente['data_nascimento'])
        self.driver.find_element_by_id('endereco-logradouro').send_keys(dados.endereco['logradouro'])
        self.driver.find_element_by_id('endereco-numero').send_keys(dados.endereco['numero'])
        self.driver.find_element_by_id('endereco-bairro').send_keys(dados.endereco['bairro'])
        self.driver.find_element_by_id('endereco-cidade').send_keys(dados.endereco['cidade'])
        self.driver.find_element_by_id('endereco-estado').send_keys(dados.endereco['estado'])
        self.driver.find_element_by_id('endereco-cep').send_keys(dados.endereco['cep'])
        self.driver.find_element_by_id('telefone').send_keys(dados.cliente['telefone'])
        self.driver.find_element_by_id('email').send_keys(dados.cliente['email'])
        self.driver.find_element_by_id('submit').click()
        time.sleep(DELAY)

    def test_cadastrar(self):
        self.login_vendedor()
        time.sleep(DELAY)
        self._cadastrar()
        confirmacao = self.driver.find_element_by_tag_name('p').text
        assert dados.cliente['documento'] in confirmacao

    def test_cadastrar_existente(self):
        self.login_vendedor()
        time.sleep(DELAY)
        self._cadastrar()
        self._cadastrar()
        erro = self.driver.find_element_by_tag_name('p').text
        assert 'já cadastrado' in erro

    def test_atualizar(self):
        self.login_vendedor()
        time.sleep(DELAY)
        self.driver.find_element_by_id('menuClientes').click()
        time.sleep(DELAY)
        self.driver.find_element_by_id('atualizarCliente').click()
        time.sleep(DELAY)
        self.driver.find_element_by_id('documento').send_keys(dados.cliente['documento'])
        self.driver.find_element_by_id('submit').click()
        time.sleep(DELAY)
        campo_email = self.driver.find_element_by_id('email')
        for i in range(20):
            campo_email.send_keys(Keys.BACKSPACE)
        self.driver.find_element_by_id('email').send_keys('novo@email.com')
        time.sleep(DELAY)
        self.driver.find_element_by_id('submit').click()
        time.sleep(DELAY)
        confirmacao = self.driver.find_element_by_tag_name('p').text
        assert 'Cliente atualizado com sucesso.' in confirmacao

    def test_atualizar_inexistente(self):
        self.login_vendedor()
        time.sleep(DELAY)
        self.driver.find_element_by_id('menuClientes').click()
        time.sleep(DELAY)
        self.driver.find_element_by_id('atualizarCliente').click()
        time.sleep(DELAY)
        self.driver.find_element_by_id('documento').send_keys('00000000')
        self.driver.find_element_by_id('submit').click()
        time.sleep(DELAY)
        erro = self.driver.find_element_by_tag_name('p').text
        assert 'Nenhum cliente encontrado.' in erro


class TestAdmin(TestBase):
    """Define os testes do menu Admin"""

    def test_consultar_vendedor(self):
        self.login_admin()
        time.sleep(DELAY)
        self.driver.find_element_by_id('menuAdmin').click()
        time.sleep(DELAY)
        self.driver.find_element_by_id('consultarVendedor').click()
        time.sleep(DELAY)
        self.driver.find_element_by_id('campo').send_keys('usuario')
        self.driver.find_element_by_id('termo').send_keys(dados.vendedor['usuario'])
        self.driver.find_element_by_id('submit').click()
        time.sleep(DELAY)
        tabela_obj = self.driver.find_elements_by_tag_name('td')
        tabela = [linha.text for linha in tabela_obj]
        assert dados.vendedor['usuario'] in tabela

    def test_consultar_vendedor_inexistente(self):
        self.login_admin()
        time.sleep(DELAY)
        self.driver.find_element_by_id('menuAdmin').click()
        time.sleep(DELAY)
        self.driver.find_element_by_id('consultarVendedor').click()
        time.sleep(DELAY)
        self.driver.find_element_by_id('campo').send_keys('usuario')
        self.driver.find_element_by_id('termo').send_keys('inexistente')
        self.driver.find_element_by_id('submit').click()
        time.sleep(DELAY)
        erro = self.driver.find_element_by_tag_name('p').text
        assert 'Nenhum vendedor encontrado.' in erro

    def _cadastrar(self):
        self.driver.find_element_by_id('menuAdmin').click()
        time.sleep(DELAY)
        self.driver.find_element_by_id('cadastrarVendedor').click()
        time.sleep(DELAY)
        self.driver.find_element_by_id('nome').send_keys(dados.vendedor_2['nome'])
        self.driver.find_element_by_id('usuario').send_keys(dados.vendedor_2['usuario'])
        self.driver.find_element_by_id('senha').send_keys(dados.vendedor_2['senha'])
        self.driver.find_element_by_id('confirma_senha').send_keys(dados.vendedor_2['senha'])
        #self.driver.find_element_by_id('admin').click()
        self.driver.find_element_by_id('submit').click()
        time.sleep(DELAY)

    def test_cadastrar_vendedor(self):
        self.login_admin()
        time.sleep(DELAY)
        self._cadastrar()
        confirmacao = self.driver.find_element_by_tag_name('p').text
        assert dados.vendedor_2['usuario'] in confirmacao

    def test_cadastrar_vendedor_existente(self):
        self.login_admin()
        time.sleep(DELAY)
        self._cadastrar()
        self._cadastrar()
        erro = self.driver.find_element_by_class_name('help-block').text
        assert 'Nome de usuário já utilizado' in erro

    def test_atualizar_vendedor(self):
        self.login_admin()
        time.sleep(DELAY)
        self.driver.find_element_by_id('menuAdmin').click()
        time.sleep(DELAY)
        self.driver.find_element_by_id('atualizarVendedor').click()
        time.sleep(DELAY)
        self.driver.find_element_by_id('id').send_keys('2')
        self.driver.find_element_by_id('submit').click()
        time.sleep(DELAY)
        campo_usuario = self.driver.find_element_by_id('usuario')
        for i in range(20):
            campo_usuario.send_keys(Keys.BACKSPACE)
        campo_usuario.send_keys('novo_usuario')
        time.sleep(DELAY)
        self.driver.find_element_by_id('submit').click()
        time.sleep(DELAY)
        confirmacao = self.driver.find_element_by_tag_name('p').text
        assert 'Vendedor atualizado com sucesso.' in confirmacao

    def test_atualizar_vendedor_inexistente(self):
        self.login_admin()
        time.sleep(DELAY)
        self.driver.find_element_by_id('menuAdmin').click()
        time.sleep(DELAY)
        self.driver.find_element_by_id('atualizarVendedor').click()
        time.sleep(DELAY)
        self.driver.find_element_by_id('id').send_keys('99')
        self.driver.find_element_by_id('submit').click()
        time.sleep(DELAY)
        erro = self.driver.find_element_by_tag_name('p').text
        assert 'Nenhum vendedor encontrado.' in erro

    def test_excluir_vendedor(self):
        self.login_admin()
        time.sleep(DELAY)
        self.driver.find_element_by_id('menuAdmin').click()
        time.sleep(DELAY)
        self.driver.find_element_by_id('excluirVendedor').click()
        time.sleep(DELAY)
        self.driver.find_element_by_id('id').send_keys(2)
        self.driver.find_element_by_id('submit').click()
        time.sleep(DELAY)
        tabela_obj = self.driver.find_elements_by_tag_name('td')
        tabela = [linha.text for linha in tabela_obj]
        assert dados.vendedor['usuario'] in tabela
        self.driver.find_element_by_id('submit').click()
        time.sleep(DELAY)
        confirmacao = self.driver.find_element_by_tag_name('p').text
        assert 'Vendedor excluido com sucesso.' in confirmacao

    def test_excluir_vendedor_inexistente(self):
        self.login_admin()
        time.sleep(DELAY)
        self.driver.find_element_by_id('menuAdmin').click()
        time.sleep(DELAY)
        self.driver.find_element_by_id('excluirVendedor').click()
        time.sleep(DELAY)
        self.driver.find_element_by_id('id').send_keys('99')
        self.driver.find_element_by_id('submit').click()
        time.sleep(DELAY)
        erro = self.driver.find_element_by_tag_name('p').text
        assert 'Nenhum vendedor encontrado.' in erro

    def test_excluir_cliente(self):
        self.login_admin()
        time.sleep(DELAY)
        self.driver.find_element_by_id('menuAdmin').click()
        time.sleep(DELAY)
        self.driver.find_element_by_id('excluirCliente').click()
        time.sleep(DELAY)
        self.driver.find_element_by_id('documento').send_keys(dados.cliente['documento'])
        self.driver.find_element_by_id('submit').click()
        time.sleep(DELAY)
        tabela_obj = self.driver.find_elements_by_tag_name('td')
        tabela = [linha.text for linha in tabela_obj]
        assert dados.cliente['documento'] in tabela
        self.driver.find_element_by_id('submit').click()
        time.sleep(DELAY)
        confirmacao = self.driver.find_element_by_tag_name('p').text
        assert 'Cliente excluido com sucesso.' in confirmacao

    def test_excluir_cliente_inexistente(self):
        self.login_admin()
        time.sleep(DELAY)
        self.driver.find_element_by_id('menuAdmin').click()
        time.sleep(DELAY)
        self.driver.find_element_by_id('excluirCliente').click()
        time.sleep(DELAY)
        self.driver.find_element_by_id('documento').send_keys('00000000')
        self.driver.find_element_by_id('submit').click()
        time.sleep(DELAY)
        erro = self.driver.find_element_by_tag_name('p').text
        assert 'Nenhum cliente encontrado.' in erro

    def test_atualizar_dados(self):
        self.login_admin()
        time.sleep(DELAY)
        self.driver.find_element_by_id('menuUsuario').click()
        time.sleep(DELAY)
        self.driver.find_element_by_id('atualizarUsuario').click()
        time.sleep(1)
        assert url_for('atualizar_vendedor') in self.driver.current_url

    def test_logout(self):
        self.login_admin()
        time.sleep(DELAY)
        self.driver.find_element_by_id('menuUsuario').click()
        time.sleep(DELAY)
        self.driver.find_element_by_id('logout').click()
        time.sleep(1)
        assert url_for('index') in self.driver.current_url



if __name__ == '__main__':
    unittest.main(verbosity=2)
