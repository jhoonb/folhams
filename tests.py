# .  Copyright (C) 2020   Jhonathan P. Banczek (jpbanczek@gmail.com)
#

import unittest
import os
import datetime

from utils import (
    str2float,
    namefile2date,
    date2filename,
    _format_item,
    format_file,
    all_files,
)
from models import Arquivo, Folha


#####################################################################
# models.py
#####################################################################
class TestModels(unittest.TestCase):

    def test_Arquivo(self):
        # criar banco
        arquivo = Arquivo(db_name="test.sqlite3")
        f = Folha(db_name="test.sqlite3")
        f.close()
        param = "WHERE 1"
        # delete
        arquivo.delete(param)
        data = [("arq1", 1_001), ("arq2", 2_001)]
        # insert
        ultimo_id = arquivo.insert(data)
        self.assertIsNot(ultimo_id, 0)
        self.assertIsNot(ultimo_id, None)

        fields, params = "descricao, itens", "where 1"
        # select
        data_db = arquivo.select(fields, params)
        self.assertEqual(data, data_db)
        # select
        fields, params = "descricao", "where 1"
        data_db = arquivo.select(fields, params)
        data = [("arq1",), ("arq2",)]
        self.assertEqual(data, data_db)
        # select
        fields, params = "descricao, itens", 'where descricao like "arq1"'
        data_db = arquivo.select(fields, params)
        data = [("arq1", 1_001)]
        self.assertEqual(data, data_db)
        # update
        data = ("arquivo-atualizado", 10_000)
        field_set = f"descricao = '{data[0]}', itens = {data[1]}" 
        params = 'where descricao like "arq1"'
        arquivo.update(field_set, params)
        fields, params = "descricao, itens", f"WHERE descricao like '{data[0]}'"
        data_db = arquivo.select(fields, params)
        self.assertEqual([data], data_db)
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
                1
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
                2
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
                2
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
                1
            ),
        ]

        ultimo_id = folha.insert(datas)
        self.assertIsNot(ultimo_id, 0)
        self.assertIsNot(ultimo_id, None)

        fields = """competencia, orgao, situacao, nome, cpf, cargo, 
        rem_base, outras_verbas, rem_posdeducoes, 
        vinculo, matricula, id_arquivo"""
        params = "where 1"
        data_db = folha.select(fields, params)
        self.assertEqual(datas, data_db)

        fields, params = "orgao", "where 1"
        data_db = folha.select(fields, params)
        self.assertEqual([(i[1],) for i in datas], data_db)
        # update
        data = ("competencia-atualizacao", 1000.50)
        field_set = f"competencia = '{data[0]}', rem_base = {data[1]}" 
        params = 'where competencia like "04/2012"'
        folha.update(field_set, params)
        fields, params = "*", f"WHERE competencia like '{data[0]}'"
        data_db = folha.select(fields, params)
        data_db = data_db[0]
        self.assertEqual(data, (data_db[1], data_db[7]))
        folha.close()


#####################################################################
# utils.py
#####################################################################
class TestUtils(unittest.TestCase):
    def test_str2float(self):
        valor = str2float("12,2")
        self.assertEqual(valor, 12.2)
        valor = str2float("12345678,77")
        self.assertEqual(valor, 12345678.77)

    def test_namefile2date(self):
        path1 = "/path/path2/path3/path4/folha-01-2000.txt"
        path2 = "path/path2/folha-02-2020.txt"
        path3 = "/path/path2/folha-03-2018.txt"
        self.assertEqual(
            datetime.datetime.strptime("01-2000", "%m-%Y"), namefile2date(path1)
        )
        self.assertEqual(
            datetime.datetime.strptime("02-2020", "%m-%Y"), namefile2date(path2)
        )
        self.assertEqual(
            datetime.datetime.strptime("03-2018", "%m-%Y"), namefile2date(path3)
        )

    def test_date2filename(self):
        _path = os.getcwd() + "/arquivos"
        path1 = f"{_path}/folha-02-2020.txt"
        path2 = f"{_path}/folha-03-2018.txt"
        path3 = f"{_path}/folha-12-2001.txt"
        self.assertEqual(
            date2filename(datetime.datetime.strptime("02-2020", "%m-%Y"), _path), path1
        )
        self.assertEqual(
            date2filename(datetime.datetime.strptime("03-2018", "%m-%Y"), _path), path2
        )
        self.assertEqual(
            date2filename(datetime.datetime.strptime("12-2001", "%m-%Y"), _path), path3
        )

    def test__format_item(self):
        s = "1{0}/201{0};orgao{0};situacao{0};nome{0};cpf{0};cargo{0};1{0},{0};100{0},{0};200{0},3{0};vinculo{0};matricula{0}"
        itens = [s.format(i) for i in range(1, 5)]
        for item in itens:
            a, b, c, d, e, f, g, h, i, j, k = item.split(";")
            g = str2float(g)
            h = str2float(h)
            i = str2float(i)
            resp = (a, b, c, d, e, f, g, h, i, j, k)
            self.assertEqual(_format_item(item), resp)

    def test_format_file(self):
        s = "1{0}/201{0};orgao{0};situacao{0};nome{0};cpf{0};cargo{0};1{0},{0};100{0},{0};200{0},3{0};vinculo{0};matricula{0}"
        itens = [s.format(i) for i in range(1, 5)]
        resp = []
        for item in itens:
            a, b, c, d, e, f, g, h, i, j, k = item.split(";")
            g = str2float(g)
            h = str2float(h)
            i = str2float(i)
            resp.append((a, b, c, d, e, f, g, h, i, j, k))
        self.assertEqual(format_file(itens), resp)

    def test_all_files(self):
        # criar diretorio e os arquivos
        path_test = f"{os.getcwd()}/test-folder"
        # os.rmdir(path_test)
        os.mkdir(path_test)
        nomes = []
        for i in range(10):
            with open("{0}/folha-09-200{1}.txt".format(path_test, i), "w") as file:
                file.write("test")
                file.flush()
            nomes.append("{0}/folha-09-200{1}.txt".format(path_test, i))

        nomes_arquivos = all_files(path=path_test)
        self.assertEqual(nomes_arquivos, nomes)
        # remove todos os arquivos criados
        for file in nomes:
            if os.path.isfile(file):
                os.remove(file)
        # exclui o diretório
        os.rmdir(path_test)


if __name__ == "__main__":
    unittest.main()
