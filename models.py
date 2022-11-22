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

class Cursos:
    def __init__(self, nome_curso, campus):
        self.nome_curso = nome_curso
        self.campus = campus

class Editais:
    def __init__(self, id, numero, nome, descricao, status, qtde_vagas, tipo, professor):
        self.id = id
        self.numero = numero
        self.nome = nome
        self.descricao = descricao
        self.status = status
        self.qtde_vagas = qtde_vagas
        self.tipo = tipo
        self.professor = professor