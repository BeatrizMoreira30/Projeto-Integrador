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
    usuario = usuario_dao.busca_id(session['usuario_logado'])
    editais = edital_dao.listar()
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


@app.route('/inscrever/<int:id>')
def inscrever(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect('/login?proxima=inscrever')
    edital = edital_dao.busca_id(id)
    usuario = usuario_dao.busca_id(session['usuario_logado'])
    return render_template('Inscrever.html', insc=edital, usuario=usuario)



@app.route('/cadastrar_edital')
def cadastrar_edital():
    usuario = usuario_dao.busca_id(session['usuario_logado'])
    if usuario._tipo != 1:
        return render_template('erro_adm.html')
    return render_template('cadastrar_edital.html')

@app.route('/novo_edital', methods=['POST',])
def novo_edital():
    numero = request.form['inputNumEdital']
    nome = request.form['inputNome']
    descricao = request.form['inputDescricao']
    status = request.form['inputGroupSelect01']
    vagas = request.form['inputVagas']
    tipo = request.form['inputTipoEdital']
    fomento = request.form['inputFomento']
    professor = request.form['inputProfessor']
    edital = Editais(numero, nome, descricao, status, vagas, tipo, fomento, professor)
    edital_dao.salvar(edital)
    return redirect('/')

if __name__ == '__main__':
    app.run()