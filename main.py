from flask import Flask, render_template, request, redirect, session, flash, url_for
import os

app = Flask(__name__)
app.secret_key = 'LP2'

from flask_mysqldb import MySQL

from models import Alunos, Editais, Cursos
from dao import alunoDao, usuarioDao, EditalDao


app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Beatriz.123456'
app.config['MYSQL_DB'] = 'Editais'
app.config['MYSQL_PORT'] = 3306
db = MySQL(app)
aluno_dao = alunoDao(db)
usuario_dao = usuarioDao(db)
edital_dao = EditalDao(db)

@app.route('/')
def index():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect('/login')
    editais = edital_dao.listar()
    usuario = usuario_dao.busca_id(session['usuario_logado'])
    return render_template('home.html', ed=editais, u=usuario)

@app.route('/login')
def login():
    proxima=request.args.get('proxima')
    if proxima == None:
        proxima=''
    return render_template('index.html', proxima=proxima)

@app.route('/autenticar', methods=['POST',])
def autenticar():
    usuario = usuario_dao.busca_id(request.form['usuario'])
    if usuario:
        if usuario._senha == request.form['senha']:
            session['usuario_logado']=request.form['usuario']
            proxima_pagina = request.form['proxima']
            if proxima_pagina == '':
                return redirect('/')
            else:
                return redirect('/{}'.format(proxima_pagina))

    flash('Não logado, tente de novo')
    return redirect('/')

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    return redirect('/login')


@app.route('/inscrever')
def inscrever():
    edital = edital_dao.busca_id(request.args.get('proximo'))
    return render_template('Inscrever.html', insc=edital)


if __name__ == '__main__':
    app.run()