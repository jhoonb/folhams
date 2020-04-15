# .  Copyright (C) 2020   Jhonathan P. Banczek (jpbanczek@gmail.com)
#

import os
import sqlite3
from typing import Iterable, List, Any
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


class Arquivo(_DBModel):
    def __init__(self, db_name="base.sqlite3"):
        super().__init__(
            db_name=db_name,
            sql_create=SQLArquivo.create,
            sql_insert=SQLArquivo.insert,
            sql_select=SQLArquivo.select,
            sql_delete=SQLArquivo.delete,
            sql_update=SQLArquivo.update,
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
            sql_create=SQLFolha.create,
            sql_insert=SQLFolha.insert,
            sql_select=SQLFolha.select,
            sql_delete=SQLFolha.delete,
            sql_update=SQLFolha.update,
        )


class Consulta(_DBModel):
    def __init__(self, db_name="base.sqlite3"):
        super().__init__(
            db_name=db_name,
            sql_create=SQLConsulta.create,
            sql_insert=SQLConsulta.insert,
            sql_select=SQLConsulta.select,
            sql_delete=SQLConsulta.delete,
            sql_update=SQLConsulta.update,
        )
