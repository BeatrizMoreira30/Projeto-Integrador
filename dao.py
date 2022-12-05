from models import Alunos, Editais, Inscricao, Cursos

SQL_CRIA_USUARIO = 'insert into Alunos (MATRICULA, NOME, CPF, EMAIL, TELEFONE, NASCIMENTO, RUA, NUMERO, CIDADE, CEP, ESTADO, PAIS, SENHA, TIPO) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
SQL_BUSCA_ID = 'select MATRICULA, NOME, CPF, EMAIL, TELEFONE, NASCIMENTO, RUA, NUMERO, CIDADE, CEP, ESTADO, PAIS, SENHA, TIPO from Alunos where MATRICULA = %s'
SQL_BUSCA_EDITAIS = 'select * from Editais'
SQL_BUSCA_EDITAL_ID = 'select * from Editais where idEDITAIS = %s'
SQL_CRIA_EDITAL = 'insert into Editais (NUMERO, NOME, DESCRICAO, STATUS, QTD_VAGAS, TIPO, FOMENTO, PROFESSOR) values (%s, %s, %s, %s, %s, %s, %s, %s)'
SQL_ATUALIZA_EDITAL = 'update Editais set NUMERO = %s, NOME = %s, DESCRICAO = %s, STATUS = %s, QTD_VAGAS =  %s, TIPO = %s, FOMENTO = %s, PROFESSOR = %s where idEDITAIS = %s'
SQL_EXCLUI_EDITAL = 'delete from Editais where idEDITAIS = %s'
SQL_CRIA_INSCRICAO = 'insert into Inscricoes (Alunos_MATRICULA, EDITAIS_idEDITAIS, CURSOS_idCURSOS) values (%s, %s, %s)'
SQL_ATUALIZA_INSCRICAO = 'update Inscricoes EDITAIS_idEDITAIS = %s, CURSOS_idCURSOS = %s where Alunos_MATRICULA = %s'
SQL_BUSCA_INSCRICOES = 'select * from Inscricoes'
SQL_BUSCA_INSCRICAO_ID = 'select * from Inscricoes where Alunos_MATRICULA = %s '
SQL_BUSCA_CURSO = 'select * from Cursos'
SQL_ATUALIZA_CURSO = 'update Cursos set  NOME_CURSO = %s, CAMPUS = %s where idCURSOS = %s'
SQL_CRIA_CURSO = 'insert into Cursos (NOME_CURSO, CAMPUS) values (%s, %s)'
SQL_BUSCA_CURSO_ID = 'select * from Cursos where idCURSOS = %s'

class alunoDao:
    def __init__(self, db):
        self.__db = db

    def salvar(self, aluno):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_CRIA_USUARIO, aluno._matricula, aluno._nome, aluno._cpf, aluno._email, aluno.telefone, aluno.nascimento, aluno.rua, aluno.numero, aluno.cidade, aluno.cep, aluno.estado, aluno.pais, aluno.senha, aluno.tipo)
        cursor._id = cursor.lastrowid

        self.__db.connection.commit()
        return aluno

class usuarioDao:
    def __init__(self, db):
        self.__db = db

    def busca_id(self, id):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_BUSCA_ID, (id,))
        dados = cursor.fetchone()
        usuario = traduz_usuario(dados) if dados else None
        return usuario

def traduz_usuario(tupla): 
    return Alunos(tupla[0], tupla[1], tupla[2], tupla[3], tupla[4], tupla[5], tupla[6], tupla[7], tupla[8], tupla[9], tupla[10], tupla[11], tupla[12], tupla[13])



class EditalDao:
    def __init__(self, db):
        self.__db = db

    def listar(self):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_BUSCA_EDITAIS)
        editais = traduz_editais(cursor.fetchall())
        return editais

    def busca_id(self, id):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_BUSCA_EDITAL_ID, (id,))
        tupla = cursor.fetchone()
        return Editais(tupla[1], tupla[2], tupla[3], tupla[4], tupla[5], tupla[6], tupla[7], tupla[8], id=tupla[0])


    
    def salvar(self, edital):
        cursor = self.__db.connection.cursor()
        if (edital.id):
            cursor.execute(SQL_ATUALIZA_EDITAL, (edital.numero, edital.nome, edital.descricao, edital.status, edital.qtde_vagas, edital.tipo, edital.fomento, edital.professor, edital.id))
        else: 
            cursor.execute(SQL_CRIA_EDITAL, (edital.numero, edital.nome, edital.descricao, edital.status, edital.qtde_vagas, edital.tipo, edital.fomento, edital.professor))
            cursor.id = cursor.lastrowid
        self.__db.connection.commit()
        return edital

    def excluir(self, id):
        self.__db.connection.cursor().execute(SQL_EXCLUI_EDITAL, (id, ))
        self.__db.connection.commit()

def traduz_edital(tupla):
    return Editais(tupla[0], tupla[1], tupla[2], tupla[3], tupla[4], tupla[5], tupla[6], tupla[7], tupla[8])

def traduz_editais(editais):
    def cria_edi_tupla(tupla):
        return Editais(tupla[1], tupla[2], tupla[3], tupla[4], tupla[5], tupla[6], tupla[7], tupla[8],  id=tupla[0])
    return list(map(cria_edi_tupla, editais))

class InscricaoDao:
    def __init__(self, db):
        self.__db = db
    
    def salvar(self, inscricao):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_CRIA_INSCRICAO, (inscricao._ra, inscricao._edital, inscricao._curso))
        cursor._id = cursor.lastrowid

        self.__db.connection.commit()

    def atualizar(self, inscricao):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_ATUALIZA_INSCRICAO, (inscricao._edital, inscricao._curso, inscricao._ra,))
        cursor._id = cursor.lastrowid

        self.__db.connection.commit()

    def busca_id(self, id):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_BUSCA_INSCRICAO_ID, (id,))
        tupla = cursor.fetchone()
        return Editais(tupla[1], tupla[2], tupla[3], tupla[4], tupla[5], tupla[6], tupla[7], tupla[8], id=tupla[0])


    def listar(self):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_BUSCA_INSCRICOES)
        inscricoes = traduz_inscricoes(cursor.fetchall())
        return inscricoes

def traduz_inscricoes(inscricoes):
    def cria_insc_tupla(tupla):
        return Inscricao(tupla[0], tupla[1], tupla[2])
    return list(map(cria_insc_tupla, inscricoes))

class CursoDao:
    def __init__(self, db):
        self.__db = db
    
    def listar(self):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_BUSCA_CURSO)
        cursos = traduz_cursos(cursor.fetchall())
        return cursos

    def busca_id(self, id):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_BUSCA_CURSO_ID, (id,))
        tupla = cursor.fetchone()
        return Cursos(tupla[1], tupla[2], id=tupla[0])

    def salvar(self, curso):
        cursor = self.__db.connection.cursor()
        if (curso._id):
            cursor.execute(SQL_ATUALIZA_CURSO, (curso._nome_curso, curso._campus, curso._id))
        else: 
            cursor.execute(SQL_CRIA_CURSO, (curso._nome_curso, curso._campus))
            cursor._id = cursor.lastrowid
        self.__db.connection.commit()
        return curso

def traduz_cursos(cursos):
    def cria_cursos_tupla(tupla):
        return Cursos(tupla[1], tupla[2], id=tupla[0])
    return list(map(cria_cursos_tupla, cursos))





