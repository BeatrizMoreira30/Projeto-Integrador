class Alunos:
    def __init__(self, matricula, nome, cpf, email, telefone, nascimento, rua, numero, cidade, cep, estado, pais, senha, tipo):
        self._matricula = matricula
        self._nome = nome
        self._cpf = cpf
        self._email = email
        self._telefone = telefone
        self._nascimento = nascimento
        self._rua = rua
        self._numero = numero
        self._cidade = cidade
        self._cep = cep
        self._estado = estado
        self._pais = pais
        self._senha = senha
        self._tipo = tipo

class Editais:
    def __init__(self, numero, nome, descricao, status, qtde_vagas, tipo, fomento, professor, id=None):
        self.id = id
        self.numero = numero
        self.nome = nome
        self.descricao = descricao
        self.status = status
        self.qtde_vagas = qtde_vagas
        self.tipo = tipo
        self.fomento = fomento
        self.professor = professor

class Inscricao:
    def __init__(self, ra, edital, curso):
        self._ra = ra
        self._edital = edital
        self._curso = curso

class Cursos:
    def __init__(self, nome_curso, campus, id=None):
        self._id = id
        self._nome_curso = nome_curso
        self._campus = campus

class Fomentos:
    def __init__(self, nome_fomento, id=None):
        self._id = id
        self._nome_fomento = nome_fomento

class Tipos:
    def __init__(self, nome_tipo, id=None):
        self._id = id
        self._nome_tipo = nome_tipo