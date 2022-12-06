from flask import Flask, render_template, request, redirect, session, flash, url_for
import os

app = Flask(__name__)
app.secret_key = 'LP2'

from flask_mysqldb import MySQL

from models import Alunos, Editais, Cursos, Inscricao, Fomentos, Tipos
from dao import usuarioDao, EditalDao, CursoDao, InscricaoDao, alunoDao, TipoDao, FomentoDao


app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Beatriz.123456'
app.config['MYSQL_DB'] = 'Editais'
app.config['MYSQL_PORT'] = 3306
db = MySQL(app)
aluno_dao = alunoDao(db)
usuario_dao = usuarioDao(db)
edital_dao = EditalDao(db)
curso_dao = CursoDao(db)
inscricao_dao = InscricaoDao(db)
tipo_dao = TipoDao(db)
fomento_dao = FomentoDao(db)

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


@app.route('/cadastrar_edital')
def cadastrar_edital():
    usuario = usuario_dao.busca_id(session['usuario_logado'])
    if usuario._tipo != 1:
        return render_template('erro_adm.html')
    tipos = tipo_dao.listar()
    return render_template('cadastrar_edital.html', tipos=tipos)

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

@app.route('/editar_edital/<int:id>')
def editar_edital(id):
    usuario = usuario_dao.busca_id(session['usuario_logado'])
    if usuario._tipo == 1:
        edital = edital_dao.busca_id(id)
        return render_template('editar_edital.html', edital=edital)

@app.route('/atualizar_edital', methods=['POST',])
def atualizar_edital():
    id = request.form['inputIdEdital']
    numero = request.form['inputNumEdital']
    nome = request.form['inputNome']
    descricao = request.form['inputDescricao']
    status = request.form['inputGroupSelect01']
    vagas = request.form['inputVagas']
    tipo = request.form['inputTipoEdital']
    fomento = request.form['inputFomento']
    professor = request.form['inputProfessor']
    edital = Editais(numero, nome, descricao, status, vagas, tipo, fomento, professor, id)
    edital_dao.salvar(edital)
    return redirect('/')


@app.route('/excluir_edital/<int:id>')
def excluir_edital(id):
    usuario = usuario_dao.busca_id(session['usuario_logado'])
    if usuario._tipo == 1:
        edital_dao.excluir(id)
        return redirect('/')

@app.route('/inscrever/<int:id>')
def inscrever(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect('/login?proxima=inscrever')
    edital = edital_dao.busca_id(id)
    usuario = usuario_dao.busca_id(session['usuario_logado'])
    cursos = curso_dao.listar()
    return render_template('Inscrever.html', insc=edital, usuario=usuario, cursos=cursos)

@app.route('/inscricao', methods=['POST',])
def inscricao():
    ra = request.form['inputRA']
    edital = request.form['idedital']
    curso = request.form['inputCurso']
    inscricao = Inscricao(ra, edital, curso)
    inscricao_dao.salvar(inscricao)
    return redirect('/')

@app.route('/cadastrar_tipo')
def cadastrar_tipo():
    usuario = usuario_dao.busca_id(session['usuario_logado'])
    if usuario._tipo != 1:
        return render_template('erro_adm.html')
    return render_template('cadastrar_tipo.html')

@app.route('/novo_tipo', methods=['POST', ])
def novo_tipo():
    nome_tipo = request.form['inputNomeTipo']
    tipo = Tipos(nome_tipo)
    tipo_dao.salvar(tipo)
    return redirect('/')
    

if __name__ == '__main__':
    app.run()