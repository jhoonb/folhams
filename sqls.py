# .  Copyright (C) 2020   Jhonathan P. Banczek (jpbanczek@gmail.com)
#

__all__ = ["SQLArquivo", "SQLFolha", "SQLConsulta"]


class SQLArquivo:
    create = """CREATE TABLE IF NOT EXISTS "Arquivo" 
  ("descricao" TEXT NOT NULL PRIMARY KEY, 
  "itens" INTEGER NOT NULL);"""

    insert = """INSERT INTO Arquivo 
  (descricao, itens) VALUES (?, ?); """

    delete = """DELETE FROM Arquivo {};"""

    select = """SELECT {} FROM Arquivo {}"""

    update = """ UPDATE Arquivo SET {} {}"""


class SQLFolha:
    create = """CREATE TABLE IF NOT EXISTS "Folha" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "competencia" TEXT NOT NULL,
    "orgao" TEXT NOT NULL,
    "situacao" TEXT NOT NULL,
    "nome" TEXT NOT NULL,
    "cpf" TEXT NOT NULL,
    "cargo" TEXT NOT NULL,
    "rem_base" REAL NOT NULL,
    "outras_verbas" REAL NOT NULL,
    "rem_posdeducoes" REAL NOT NULL,
    "vinculo" TEXT NOT NULL,
    "matricula" TEXT NOT NULL); """

    insert = """INSERT INTO Folha (competencia, orgao, 
  situacao, nome, cpf, cargo, rem_base, outras_verbas,
  rem_posdeducoes, vinculo, matricula) 
  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?); """

    delete = """DELETE FROM Folha {};"""

    select = """SELECT {} FROM Folha {}"""

    update = """ UPDATE Folha SET {} {}"""


class SQLConsulta:
    create = """CREATE TABLE IF NOT EXISTS "Consulta" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "query" TEXT NOT NULL,
    "resultado" TEXT NOT NULL);"""

    insert = """INSERT INTO Consulta 
  (query, resultado) VALUES (?, ?); """

    delete = """DELETE FROM Consulta {};"""

    select = """SELECT {} from Consulta {};"""

    update = """ UPDATE Consulta SET {} {};"""