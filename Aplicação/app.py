"""
app.py

Instancia app, para desenvolvimento.

Para iniciar a aplicação, execute o arquivo ou use o comando: flask run
Para executar os testes unitários, use o comando: flask test
"""

import click
from sys import argv
import livraria
from livraria import app


@app.cli.command()
@click.argument('test_names', nargs=-1)
def test(test_names):
    """Executa os testes unitários"""
    import unittest
    livraria.set_config('testes')
    if test_names:
        tests = unittest.TestLoader().loadTestsFromNames(test_names)
    else:
        tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    """Inicializa a aplicação web"""
    livraria.set_config('dev')
    app.run(debug=True)