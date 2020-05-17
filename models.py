# .  Copyright (C) 2020   Jhonathan P. Banczek (jpbanczek@gmail.com)
#

import os
import sqlite3
from typing import Iterable, List, Any


__all__ = ["Arquivo", "Folha"]

#####################################################################
# class exception
#####################################################################
class _DBError(ValueError):
    pass


#####################################################################
# classes SQLs
#####################################################################
class _SQLArquivo:
    create = """CREATE TABLE IF NOT EXISTS "Arquivo" 
  ("id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "descricao" TEXT NOT NULL, 
  "itens" INTEGER NOT NULL);"""

    insert = """INSERT INTO Arquivo 
  (descricao, itens) VALUES (?, ?); """

    delete = """DELETE FROM Arquivo {}; """

    select = """SELECT {} FROM Arquivo {}"""

    update = """ UPDATE Arquivo SET {} {}"""


class _SQLFolha:
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
    "matricula" TEXT NOT NULL,
    "id_arquivo" INTEGER NOT NULL); """

    insert = """INSERT INTO Folha (competencia, orgao, 
  situacao, nome, cpf, cargo, rem_base, outras_verbas,
  rem_posdeducoes, vinculo, matricula, id_arquivo) 
  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?); """

    delete = """DELETE FROM Folha {};"""

    select = """SELECT {} FROM Folha f {}"""

    update = """ UPDATE Folha SET {} {}"""


#####################################################################
# class model abstract
#####################################################################
class _DBModel:
    def __init__(
        self,
        db_name: str = "base.sqlite3",
        sql_create: str = None,
        sql_insert: str = None,
        sql_select: str = None,
        sql_delete: str = None,
        sql_update: str = None,
    ):
        self._db_path = os.path.join(os.path.dirname(__file__), db_name)
        self._conn = sqlite3.connect(self._db_path)
        self._cursor = self._conn.cursor()
        self._sql_create = sql_create
        self._sql_insert = sql_insert
        self._sql_select = sql_select
        self._sql_delete = sql_delete
        self._sql_update = sql_update
        self._create()

    def _create(self) -> None:
        try:
            self._cursor.execute(self._sql_create)
            self._conn.commit()
        except:
            self._conn.rollback()
            raise _DBError("Problema ao criar tabela")

    def insert(self, data: Iterable[Iterable] = None) -> int:
        lastrowid = None
        try:
            for d in data:
                self._cursor.execute(self._sql_insert, d)
                lastrowid = self._cursor.lastrowid
            self._conn.commit()
        except:
            self._conn.rollback()
            raise _DBError("Problema ao inserir dados na tabela")
        return lastrowid

    def select(self, fields: str = None, params: str = None) -> List[Any]:
        try:
            data = self._cursor.execute(self._sql_select.format(fields, params))
            data = data.fetchall()
        except:
            raise _DBError("Problema executar select")
        return data

    def delete(self, params: str = None) -> None:
        try:
            self._cursor.execute(self._sql_delete.format(params))
            self._conn.commit()
        except:
            self._conn.rollback()
            raise _DBError("Problema ao deletar dados")

    def update(self, field_set: str = None, params: str = None) -> None:
        try:
            sql = self._sql_update.format(field_set, params)
            self._cursor.execute(sql)
        except:
            self._conn.rollback()
            raise _DBError("Problema ao atualizar tabela")

    def close(self):
        self._cursor.close()
        self._conn.commit()
        self._conn.close()


#####################################################################
# classes
#####################################################################
class Arquivo(_DBModel):
    def __init__(self, db_name="base.sqlite3"):
        super().__init__(
            db_name=db_name,
            sql_create=_SQLArquivo.create,
            sql_insert=_SQLArquivo.insert,
            sql_select=_SQLArquivo.select,
            sql_delete=_SQLArquivo.delete,
            sql_update=_SQLArquivo.update,
        )

    def delete(self, params: str = None) -> None:
        super().delete(params=params)
        try:
            sql = """DELETE FROM Folha WHERE Folha.id in 
            (SELECT Folha.id FROM Folha WHERE Folha.id_arquivo not in 
            (select Arquivo.id from Arquivo));"""
            self._cursor.execute(sql)
            self._conn.commit()
        except:
            raise _DBError("Problema executar exclusão do relacionamento ")


class Folha(_DBModel):
    def __init__(self, db_name="base.sqlite3"):
        super().__init__(
            db_name=db_name,
            sql_create=_SQLFolha.create,
            sql_insert=_SQLFolha.insert,
            sql_select=_SQLFolha.select,
            sql_delete=_SQLFolha.delete,
            sql_update=_SQLFolha.update,
        )