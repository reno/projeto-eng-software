# Projeto final: Engenharia de Software - GCC188

**Alunos:** Renan Modenese e Gabriel Amorim

**Projeto:** Livraria do Amorim

Sistema de controle de vendas para livraria, incluindo base de dados de livros, vendedores, clientes e pedidos. A aplicação web utiliza a linguagem python e o microframework Flask, além de HTML, Bootstrap e Javascript para o front-end.



## Releases

*  **v0.1**: Documentação de requisitos e protótipo da interface.
*  **v1**: Documentação de projeto incluindo diagramas de classes e de sequência, além da implementação da interface e operações sobre a tabela Livros. 



## Estrutura da aplicação

O projeto é organizado conforme abaixo:

```
/projeto_eng_software/Aplicação/
├── livraria/
│   ├── __init__.py
│   ├── forms.py
│   ├── models.py
│   ├── tables.py
│   ├── views.py
│   └── templates/
├── tests/
├── create_db.py
├── config.py
└── app.py 
```

Uma breve descrição de arquivos e pastas:

* `livraria/` é o pacote que contém a aplicação.
* `__init__.py` código de inicialização do pacote. 
* `forms.py` guarda as definições dos formulários utilizados.
* `models.py` contém as definições das tabelas do banco de dados.
* `tables.py` guarda definições de tabelas usadas na renderização do resultado de consultas.
* `views.py` controla as rotas da aplicação.
* `templates/` contém todos os arquivos HTML utilizados.
* `tests/` contém o código de testes.
* `create_db.py` script de inicialização do banco de dados no ambiente de desenvolvimento.
* `config.py` guarda configurações de diferentes ambientes, como desenvolvimento e testes.
* `app.py` código que instancia a aplicação.



## Requisitos

* **Python 3.4+**

  Para instalar ou atualizar, no Linux, use: `sudo apt-get install python`
  
* **pip**

  Gerenciador de pacotes do python. Para instalar ou atualizar, no Linux, use: `sudo apt install python3-pip`

* **venv**

  No Ubuntu o gerenciador de ambiente virtual não é instalado por padrão. Para instalar, use: `sudo apt-get install python3-venv`

* **Banco de dados PostgreSQL ou SQLite**

  A aplicação é pré-configurada para o PostgreSQL no ambiente de desenvolvimento, e inclui as configurações para uso do SQLite. Instruções de instalação do PostgreSQL ser encontradas [aqui](https://www.postgresql.org/download/).
  
  Para instalar o SQLite, no Linux, basta utilizar os comandos `apt-get install sqlite3` e   `apt-get install libsqlite3-dev`.

## Uso
  
**1. Configuração do ambiente virtual**

Faça o clone do repositório:

`git clone https://github.com/reno/projeto_eng_software.git`

Vá para a pasta da aplicação:

`cd Aplicação`

Crie um ambiente virtual:

`python3 -m venv venv`

Ative o ambiente virtual:

`source venv/bin/activate`

Instale as dependências no ambiente virtual:

`pip install -r requirements.txt`

  
**2. Inicialização do banco de dados (opcional)**

Caso deseje inicializar o banco de dados, execute:

`python create_db.py`

As configurações do banco de dados estão localizadas no arquivo `config.py`.

  
**3. Execução da aplicação**

Finalmente, execute:

`python app.py dev`

A aplicação poderá ser acessada por um navegador no endereço `http://localhost:5000`



## Colaboração

Ao realizar um commit, indique na mensagem o fechamento da issue relacionada (caso possua) usando `Closes #1`, com o número da Issue. Isso fechará o Issue automaticamente.

Em seguida, localize no backlog a issue fechada  e inclua um comentário com o hash do commit.
