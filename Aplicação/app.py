'''
app.py

Instancia app, para desenvolvimento. Recebe argumento ('dev', 'testes' ou 'producao').
'''

import click
from sys import argv
import livraria
if argv[1]: livraria.set_config(argv[1])
#livraria.set_config('base')
from livraria import app


@app.cli.command()
@click.argument('test_names', nargs=-1)
def test(test_names):
    """Executa os testes unitários"""
    import unittest
    if test_names:
        tests = unittest.TestLoader().loadTestsFromNames(test_names)
    else:
        tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    app.run(debug=True)