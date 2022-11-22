from models import Alunos, Editais

SQL_CRIA_USUARIO = 'insert into Alunos (MATRICULA, NOME, CPF, EMAIL, TELEFONE, NASCIMENTO, RUA, NUMERO, CIDADE, CEP, ESTADO, PAIS, SENHA) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
SQL_BUSCA_ID = 'select MATRICULA, NOME, CPF, EMAIL, TELEFONE, NASCIMENTO, RUA, NUMERO, CIDADE, CEP, ESTADO, PAIS, SENHA from Alunos where MATRICULA = %s'

class alunoDao:
    def __init__(self, db):
        self.__db = db

    def salvar(self, aluno):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_CRIA_USUARIO, aluno._matricula, aluno._nome, aluno._cpf, aluno._email, aluno.telefone, aluno.nascimento, aluno.rua, aluno.numero, aluno.cidade, aluno.cep, aluno.estado, aluno.pais, aluno.senha)
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
    return Alunos(tupla[0], tupla[1], tupla[2], tupla[3], tupla[4], tupla[5], tupla[6], tupla[7], tupla[8], tupla[9], tupla[10], tupla[11], tupla[12])