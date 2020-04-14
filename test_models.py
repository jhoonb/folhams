# .  Copyright (C) 2020   Jhonathan P. Banczek (jpbanczek@gmail.com)
#

import unittest
from models import Arquivo, Folha, Consulta


class TestModels(unittest.TestCase):
    def test_Arquivo(self):
        arquivo = Arquivo(db_name="test.sqlite3")
        param = "WHERE 1"
        arquivo.delete(param)
        data = [("arq1", 1_001), ("arq2", 2_001)]
        arquivo.insert(data)
        fields, params = "descricao, itens", "where 1"
        data_db = arquivo.select(fields, params)
        self.assertEqual(data, data_db)

        fields, params = "descricao", "where 1"
        data_db = arquivo.select(fields, params)
        data = [("arq1",), ("arq2",)]
        self.assertEqual(data, data_db)

        fields, params = "descricao, itens", 'where descricao like "arq1"'
        data_db = arquivo.select(fields, params)
        data = [("arq1", 1_001)]
        self.assertEqual(data, data_db)
        arquivo.close()

    def test_Folha(self):
        folha = Folha(db_name="test.sqlite3")
        param = "WHERE 1"
        folha.delete(param)

        datas = [
            (
                "01/2012",
                "orgaox",
                "situacaox",
                "nomex",
                "cpfx",
                "cargox",
                1000.1,
                50.5,
                1235.9,
                "vinculox",
                "matriculax",
            ),
            (
                "02/2012",
                "orgaoy",
                "situacaoy",
                "nomey",
                "cpfy",
                "cargoy",
                1000.2,
                60.5,
                2222.2,
                "vinculoy",
                "matriculay",
            ),
            (
                "03/2012",
                "orgaoz",
                "situacaoz",
                "nomez",
                "cpfz",
                "cargoz",
                1000.3,
                70.5,
                3333.3,
                "vinculoz",
                "matriculaz",
            ),
            (
                "04/2012",
                "orgaow",
                "situacaow",
                "nomew",
                "cpfw",
                "cargozw",
                1000.4,
                80.5,
                4444.4,
                "vinculow",
                "matriculaw",
            ),
        ]

        folha.insert(datas)

        fields = """competencia, orgao, situacao, nome, cpf, cargo, 
        rem_base, outras_verbas, rem_posdeducoes, vinculo, matricula"""
        params = "where 1"
        data_db = folha.select(fields, params)
        self.assertEqual(datas, data_db)

        fields, params = "orgao", "where 1"
        data_db = folha.select(fields, params)
        self.assertEqual([(i[1],) for i in datas], data_db)
        folha.close()

    def test_Consulta(self):
        consulta = Consulta(db_name="test.sqlite3")
        param = "WHERE 1"
        consulta.delete(param)
        data = [
            ("query1", "resultado1"),
            ("query2", "resultado2"),
            ("query3", "resultado3"),
            ("query4", "resultado4"),
        ]
        consulta.insert(data)

        fields, params = "resultado", "where 1"
        data_db = consulta.select(fields, params)
        self.assertEqual([(i[1],) for i in data], data_db)

        fields, params = "query", "where 1"
        data_db = consulta.select(fields, params)
        self.assertEqual([(i[0],) for i in data], data_db)
        consulta.close()


if __name__ == "__main__":
    unittest.main()
