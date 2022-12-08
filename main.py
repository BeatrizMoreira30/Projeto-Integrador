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
    fomentos = fomento_dao.listar()
    return render_template('cadastrar_edital.html', tipos=tipos, fomentos=fomentos)

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
    inscricao = inscricao_dao.busca_id(usuario._matricula, id)
    return render_template('Inscrever.html', insc=edital, usuario=usuario, cursos=cursos, inscricao=inscricao)

@app.route('/inscricao', methods=['POST',])
def inscricao():
    ra = request.form['inputRA']
    edital = request.form['idedital']
    curso = request.form['inputCurso']
    inscricao = Inscricao(ra, edital, curso)
    inscricao_dao.salvar(inscricao)
    return redirect('/')

@app.route('/ver_inscricoes')
def ver_inscricoes():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect('/login?proxima=ver_inscricoes')
    usuario = usuario_dao.busca_id(session['usuario_logado'])
    inscricoes = inscricao_dao.listar(usuario._matricula)
    editais = edital_dao.listar()
    return render_template('minhas_inscricoes.html', inscricoes=inscricoes, editais=editais)

@app.route('/editar_inscricao/<int:id>')
def editar_inscricao(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect('/login?proxima=ver_inscricoes')
    usuario = usuario_dao.busca_id(session['usuario_logado'])
    edital = edital_dao.busca_id(id)
    inscricao = inscricao_dao.busca_id(usuario._matricula, id)
    cursos = curso_dao.listar()
    return render_template('editar_inscricao.html', inscricao=inscricao, edital=edital, cursos=cursos)

@app.route('/atualizar_inscricao', methods=['POST', ])
def atualizar_inscricao():
    ra = request.form['inputRA']
    edital = request.form['idedital']
    curso = request.form['inputCurso']
    inscricao = Inscricao(ra, edital, curso)
    inscricao_dao.atualizar(inscricao)
    return redirect('/ver_inscricoes')

@app.route('/excluir_inscricao/<int:id>')
def excluir_inscricao(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect('/login?proxima=ver_inscricoes')
    usuario = usuario_dao.busca_id(session['usuario_logado'])
    inscricao_dao.excluir(usuario._matricula, id)
    return redirect('/ver_inscricoes')

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

@app.route('/edit_tipo')
def edit_tipo():
    usuario = usuario_dao.busca_id(session['usuario_logado'])
    if usuario._tipo == 1:
        tipos = tipo_dao.listar()
        return render_template('atualizar_tipo.html', tipos=tipos)

@app.route('/editar_tipo', methods=['POST', ])
def editar_tipo():
    usuario = usuario_dao.busca_id(session['usuario_logado'])
    if usuario._tipo == 1:
        id = request.form['inputTipo']
        tipo = tipo_dao.busca_id(id)
        return render_template('editar_tipo.html', tipo=tipo)

@app.route('/atualizar_tipo', methods=['POST',])
def atualizar_tipo():
    id = request.form['idTipo']
    nome_tipo = request.form['inputNomeTipo']
    tipo = Tipos(nome_tipo, id)
    tipo_dao.salvar(tipo)
    return redirect('/edit_tipo')

@app.route('/excluir_tipo')
def excluir_tipo():
    usuario = usuario_dao.busca_id(session['usuario_logado'])
    if usuario._tipo == 1:
        tipos = tipo_dao.listar()
        return render_template('excluir_tipo.html', tipos=tipos)

@app.route('/delete_tipo', methods=['POST', ])
def delete_tipo():
    id = request.form['inputTipo']
    tipo_dao.excluir(id)
    return redirect('/excluir_tipo')

@app.route('/cadastrar_fomento')
def cadastrar_fomento():
    usuario = usuario_dao.busca_id(session['usuario_logado'])
    if usuario._tipo != 1:
        return render_template('erro_adm.html')
    return render_template('cadastrar_fomento.html')

@app.route('/novo_fomento', methods=['POST', ])
def novo_fomento():
    nome_fomento = request.form['inputNomeFomento']
    fomento = Fomentos(nome_fomento)
    fomento_dao.salvar(fomento)
    return redirect('/')

@app.route('/edit_fomento')
def edit_fomento():
    usuario = usuario_dao.busca_id(session['usuario_logado'])
    if usuario._tipo == 1:
        fomentos = fomento_dao.listar()
        return render_template('atualizar_fomento.html', fomentos=fomentos)

@app.route('/editar_fomento', methods=['POST', ])
def editar_fomento():
    usuario = usuario_dao.busca_id(session['usuario_logado'])
    if usuario._tipo == 1:
        id = request.form['inputFomento']
        fomento = fomento_dao.busca_id(id)
        return render_template('editar_fomento.html', fomento=fomento)

@app.route('/atualizar_fomento', methods=['POST',])
def atualizar_fomento():
    id = request.form['idFomento']
    nome_fomento = request.form['inputNomeFomento']
    fomento = Fomentos(nome_fomento, id)
    fomento_dao.salvar(fomento)
    return redirect('/edit_fomento')

@app.route('/excluir_fomento')
def excluir_fomento():
    usuario = usuario_dao.busca_id(session['usuario_logado'])
    if usuario._tipo == 1:
        fomentos = fomento_dao.listar()
        return render_template('excluir_fomento.html', fomentos=fomentos)

@app.route('/delete_fomento', methods=['POST', ])
def delete_fomento():
    id = request.form['inputFomento']
    fomento_dao.excluir(id)
    return redirect('/excluir_fomento')


@app.route('/cadastrar_curso')
def cadastrar_curso():
    usuario = usuario_dao.busca_id(session['usuario_logado'])
    if usuario._tipo != 1:
        return render_template('erro_adm.html')
    return render_template('cadastrar_curso.html')

@app.route('/novo_curso', methods=['POST', ])
def novo_curso():
    nome_curso = request.form['inputNomeCurso']
    campus = request.form['inputCampus']
    curso = Cursos(nome_curso, campus)
    curso_dao.salvar(curso)
    return redirect('/cadastrar_curso')

@app.route('/edit_curso')
def edit_curso():
    usuario = usuario_dao.busca_id(session['usuario_logado'])
    if usuario._tipo == 1:
        cursos = curso_dao.listar()
        return render_template('atualizar_curso.html', cursos=cursos)

@app.route('/editar_curso', methods=['POST', ])
def editar_curso():
    usuario = usuario_dao.busca_id(session['usuario_logado'])
    if usuario._tipo == 1:
        id = request.form['inputCurso']
        curso = curso_dao.busca_id(id)
        return render_template('editar_curso.html', curso=curso)

@app.route('/atualizar_curso', methods=['POST',])
def atualizar_curso():
    id = request.form['idCurso']
    nome_curso = request.form['inputNomeCurso']
    nome_campus = request.form['inputNomeCampus']
    curso = Cursos(nome_curso, nome_campus, id)
    curso_dao.salvar(curso)
    return redirect('/edit_curso')

@app.route('/excluir_curso')
def excluir_curso():
    usuario = usuario_dao.busca_id(session['usuario_logado'])
    if usuario._tipo == 1:
        cursos = curso_dao.listar()
        return render_template('excluir_curso.html', cursos=cursos)

@app.route('/delete_curso', methods=['POST', ])
def delete_curso():
    id = request.form['inputCurso']
    curso_dao.excluir(id)
    return redirect('/excluir_curso')
    

if __name__ == '__main__':
    app.run()