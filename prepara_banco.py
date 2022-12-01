import MySQLdb
print('Conectando...')
conn = MySQLdb.connect(user='root', passwd='Beatriz.123456', host='127.0.0.1', port=3306, charset='utf8')

conn.cursor().execute("DROP DATABASE `Editais`;")
conn.commit()

criar_tabelas = '''CREATE SCHEMA IF NOT EXISTS `Editais` DEFAULT CHARACTER SET utf8 ;
USE `Editais` ;

CREATE TABLE IF NOT EXISTS `Editais`.`Alunos` (
  `MATRICULA` CHAR(11) NOT NULL,
  `NOME` VARCHAR(45) NOT NULL,
  `CPF` VARCHAR(45) NOT NULL,
  `EMAIL` VARCHAR(45) NOT NULL,
  `TELEFONE` VARCHAR(45) NULL,
  `NASCIMENTO` DATE NOT NULL,
  `RUA` VARCHAR(45) NULL,
  `NUMERO` VARCHAR(6) NULL,
  `CIDADE` VARCHAR(45) NULL,
  `CEP` VARCHAR(45) NULL,
  `ESTADO` VARCHAR(20) NULL,
  `PAIS` VARCHAR(45) NULL,
  `SENHA` VARCHAR(45) NOT NULL,
  `TIPO` TINYINT NOT NULL,
  PRIMARY KEY (`MATRICULA`))
ENGINE = InnoDB;


CREATE TABLE IF NOT EXISTS `Editais`.`Cursos` (
  `idCURSOS` INT NOT NULL,
  `NOME_CURSO` VARCHAR(45) NOT NULL,
  `CAMPUS` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idCURSOS`))
ENGINE = InnoDB;


CREATE TABLE IF NOT EXISTS `Editais`.`Editais` (
  `idEDITAIS` INT NOT NULL AUTO_INCREMENT,
  `NUMERO` VARCHAR(45) NULL,
  `NOME` VARCHAR(1000) NULL,
  `DESCRICAO` VARCHAR(1000) NULL,
  `STATUS` VARCHAR(45) NULL,
  `QTD_VAGAS` INT NULL,
  `TIPO` VARCHAR(45) NULL,
  `FOMENTO` VARCHAR(45) NULL,
  `PROFESSOR` VARCHAR(45) NULL,
  PRIMARY KEY (`idEDITAIS`))
ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `Editais`.`Inscricoes` (
  `Alunos_MATRICULA` CHAR(11) NOT NULL,
  `EDITAIS_idEDITAIS` INT NOT NULL,
  `CURSOS_idCURSOS` INT NOT NULL,
  PRIMARY KEY (`Alunos_MATRICULA`, `EDITAIS_idEDITAIS`),
  INDEX `fk_Alunos_has_EDITAIS_EDITAIS1_idx` (`EDITAIS_idEDITAIS` ASC) VISIBLE,
  INDEX `fk_Alunos_has_EDITAIS_Alunos_idx` (`Alunos_MATRICULA` ASC) VISIBLE,
  INDEX `fk_Alunos_has_EDITAIS_CURSOS1_idx` (`CURSOS_idCURSOS` ASC) VISIBLE,
  CONSTRAINT `fk_Alunos_has_EDITAIS_Alunos`
    FOREIGN KEY (`Alunos_MATRICULA`)
    REFERENCES `Editais`.`Alunos` (`MATRICULA`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Alunos_has_EDITAIS_EDITAIS1`
    FOREIGN KEY (`EDITAIS_idEDITAIS`)
    REFERENCES `Editais`.`Editais` (`idEDITAIS`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Alunos_has_EDITAIS_CURSOS1`
    FOREIGN KEY (`CURSOS_idCURSOS`)
    REFERENCES `Editais`.`Cursos` (`idCURSOS`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;'''

conn.cursor().execute(criar_tabelas)

cursor = conn.cursor()
cursor.executemany(
    'INSERT INTO Alunos (MATRICULA, NOME, CPF, EMAIL, TELEFONE, NASCIMENTO, RUA, NUMERO, CIDADE, CEP, ESTADO, PAIS, SENHA, TIPO) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',  
    [
        ('20211340021', 'Beatriz Moreira', '123456789', 'bia30.albano', '99656565', '20011030', 'Av Rebeca', '578', 'Muzambinho', '37789000', 'MG', 'Brasil', 'bia', 1),
        ('20211340025', 'Beatriz Albano', '123456789', 'bia30.albano', '99656565', '20011030', 'Av Rebeca', '578', 'Muzambinho', '37789000', 'MG', 'Brasil', '123456', 0)
    ]
)



conn.commit()
cursor.close()

