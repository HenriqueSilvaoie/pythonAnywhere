# A very simple Flask Hello World app for you to get started with...
from flask import Flask, request, redirect, abort, make_response
app = Flask(__name__)
@app.route('/')
def hello_world():
#    return '<p>Alterações por meio do PythonAnyWhere -> GitHub</p><table><tr><td><b>Professor:</b></td><td>Professor Fabio Teixeira</td></tr><tr><td><b>Prontuário:</b></td><td>PT23820X</td></tr></table>'
    return '<h1>Hello World!</h1><h2>Disciplina PTBDSWS</h2>'

@app.route('/user/<name>')
def user(name):
    return '<h1>Hello, {}!</h1>'.format(name)

@app.route('/contextorequisicao')
def contextorequisicao():
    user_agent = request.headers.get('User-Agent')
    return '<p>Your browser is {}</p>'.format(user_agent)

@app.route('/codigostatusdiferente')
def codigostatusdiferente():
    return '<p>Bad request</p>', 400

@app.route('/redirecionamento')
def redirecionamento():
    return redirect('https://ptb.ifsp.edu.br')

@app.route('/abortar')
def abortar():
    return abort(404)

@app.route('/objetoresposta')
def objeto_resposta():
    #objeto de resposta
    response = make_response('<h1>This document carries a cookie!</h1>')

    #gera o cookie
    response.set_cookie('answer', '42')

    return response