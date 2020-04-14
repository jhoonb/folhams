# .  Copyright (C) 2020   Jhonathan P. Banczek (jpbanczek@gmail.com)
#

import os
import sqlite3
from typing import Iterable
from sqls import SQLArquivo, SQLFolha, SQLConsulta


__all__ = ["Arquivo", "Folha", "Consulta"]


class _DBError(ValueError):
    pass


class _DBModel:
    def __init__(
        self,
        db_name: str = "base.sqlite3",
        sql_create: str = None,
        sql_insert: str = None,
        sql_select: str = None,
        sql_delete: str = None,
    ):
        self._db_path = os.path.join(os.path.dirname(__file__), db_name)
        self._conn = sqlite3.connect(self._db_path)
        self._cursor = self._conn.cursor()
        self._sql_create = sql_create
        self._sql_insert = sql_insert
        self._sql_select = sql_select
        self._sql_delete = sql_delete
        self._create()

    def _create(self):
        try:
            self._cursor.execute(self._sql_create)
            self._conn.commit()
        except:
            self._conn.rollback()
            raise _DBError("Problema ao criar tabela")

    def insert(self, data: Iterable[Iterable]):
        try:
            self._cursor.executemany(self._sql_insert, data)
            self._conn.commit()
        except:
            self._conn.rollback()
            raise _DBError("Problema ao inserir dados na tabela")

    def select(self, fields, params):
        try:
            data = self._cursor.execute(self._sql_select.format(fields, params))
            data = data.fetchall()
        except:
            raise _DBError("Problema executar select")
        return data

    def delete(self, param):
        try:
            self._cursor.execute(self._sql_delete.format(param))
            self._conn.commit()
        except:
            self._conn.rollback()
            raise _DBError("Problema ao deletar dados")

    def execute_sql(self, sql, params):
        try:
            data = self._cursor.execute(sql, params)
            data = data.fetchall()
        except:
            self._conn.rollback()
            raise _DBError("Problema ao executar sql")
        return data

    def executemany_sql(self, sql, params):
        try:
            data = self._cursor.executemany(sql, params)
            data = data.fetchall()
        except:
            self._conn.rollback()
            raise _DBError("Problema ao executar sql")
        return data

    def close(self):
        self._cursor.close()
        self._conn.commit()
        self._conn.close()


class Arquivo(_DBModel):
    def __init__(self, db_name="base.sqlite3"):
        super().__init__(
            db_name=db_name,
            sql_create=SQLArquivo.create,
            sql_insert=SQLArquivo.insert,
            sql_select=SQLArquivo.select,
            sql_delete=SQLArquivo.delete,
        )


class Folha(_DBModel):
    def __init__(self, db_name="base.sqlite3"):
        super().__init__(
            db_name=db_name,
            sql_create=SQLFolha.create,
            sql_insert=SQLFolha.insert,
            sql_select=SQLFolha.select,
            sql_delete=SQLFolha.delete,
        )


class Consulta(_DBModel):
    def __init__(self, db_name="base.sqlite3"):
        super().__init__(
            db_name=db_name,
            sql_create=SQLConsulta.create,
            sql_insert=SQLConsulta.insert,
            sql_select=SQLConsulta.select,
            sql_delete=SQLConsulta.delete,
        )
