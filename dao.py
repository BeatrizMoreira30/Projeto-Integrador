from models import Alunos, Editais

SQL_CRIA_USUARIO = 'insert into Alunos (MATRICULA, NOME, CPF, EMAIL, TELEFONE, NASCIMENTO, RUA, NUMERO, CIDADE, CEP, ESTADO, PAIS, SENHA, TIPO) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
SQL_BUSCA_ID = 'select MATRICULA, NOME, CPF, EMAIL, TELEFONE, NASCIMENTO, RUA, NUMERO, CIDADE, CEP, ESTADO, PAIS, SENHA, TIPO from Alunos where MATRICULA = %s'
SQL_BUSCA_EDITAIS = 'select * from Editais'
SQL_BUSCA_EDITAL_ID = 'select idEDITAIS, NUMERO, NOME, DESCRICAO, STATUS, QTD_VAGAS, TIPO, FOMENTO, PROFESSOR from Editais where idEDITAIS = %s'
SQL_CRIA_EDITAL = 'insert into Editais (NUMERO, NOME, DESCRICAO, STATUS, QTD_VAGAS, TIPO, FOMENTO, PROFESSOR, idEDITAIS) values (%s, %s, %s, %s, %s, %s, %s, %s)'
SQL_ATUALIZA_EDITAL = 'update Editais set NUMERO = %s, NOME = %s, DESCRICAO = %s, STATUS = %s, QTD_VAGAS =  %s, TIPO = %s, FOMENTO = %s, PROFESSOR = %s, idEDITAIS = %s'

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

def traduz_edital(tupla):
    return Editais(tupla[0], tupla[1], tupla[2], tupla[3], tupla[4], tupla[5], tupla[6], tupla[7], tupla[8])

def traduz_editais(editais):
    def cria_edi_tupla(tupla):
        return Editais(tupla[1], tupla[2], tupla[3], tupla[4], tupla[5], tupla[6], tupla[7], tupla[8],  id=tupla[0])
    return list(map(cria_edi_tupla, editais))