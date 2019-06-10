
from flask import Flask, render_template
from livraria import app, views

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404