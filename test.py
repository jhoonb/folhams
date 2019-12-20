import os
import unittest
import requests
import folhams
import pathlib


class TestScrapFunctions(unittest.TestCase):

    def test_url_gov(self):
        url = 'http://www.dados.ms.gov.br/dataset/folha-de-pagamento'
        self.assertEqual(folhams.url_gov(), url)

    def test_get_page_text(self):
        r = requests.get(folhams.url_gov())
        self.assertEqual(r.url, folhams.url_gov())

    # [TODO]
    def test_get_online(self):
        self.assertEqual(folhams.get_online(), True)


class TestFilesOsFunctions(unittest.TestCase):

    def test_link_to_path_files(self):
        link = folhams.link_to_path_files()
        link = link.split("/")[-2]
        self.assertEqual(link, "arquivos")

    def test_read_file(self):

        file_test = 'test_read_file.txt'
        with open(file_test, 'w') as f:
            f.write('cabeçalho\n')
            f.flush()
            f.write("read_file_test")

        p = pathlib.Path(file_test)
        data = folhams.read_file(p)
        # delete file
        os.remove(file_test)
        self.assertEqual(data, ["read_file_test"])

    def test_get_all_files(self):
        pass


class TestModels(unittest.TestCase):

    def test_str2float(self):
        self.assertEqual(folhams._str2float("'200,50'"), 200.50)
        self.assertEqual(folhams._str2float('"200,50"'), 200.50)
        self.assertEqual(folhams._str2float("'23,58'"), 23.58)
        self.assertEqual(folhams._str2float('"23,58"'), 23.58)
        self.assertEqual(folhams._str2float("'10000000,58'"), 10000000.58)
        self.assertEqual(folhams._str2float('"10000000,58"'), 10000000.58)

    def test_FolhaItem(self):
        s = '01/2018;AGEPREV;INATIVO - APOSENTADO;ALONZO CHURCH;123.***.***-123;AUXILIAR DE PROVAS AUTOMATICAS DE TEOREMAS;"1493,24";"200,00";"1693,24";ESTATUTARIO;000000000'

        fi = folhams._FolhaItem(s)

        comp = folhams._Competencia('01', '2018', '')

        self.assertEqual(fi.competencia.mes, comp.mes)
        self.assertEqual(fi.competencia.ano, comp.ano)
        self.assertEqual(fi.competencia.tipo, comp.tipo)

        self.assertEqual(fi.orgao, "AGEPREV")
        self.assertEqual(fi.situacao, "INATIVO - APOSENTADO")
        self.assertEqual(fi.nome, "ALONZO CHURCH")
        self.assertEqual(fi.cpf, "123.***.***-123")
        self.assertEqual(
            fi.cargo, "AUXILIAR DE PROVAS AUTOMATICAS DE TEOREMAS")
        self.assertEqual(fi.rem_base, 1493.24)
        self.assertEqual(fi.outras_verbas, 200.00)
        self.assertEqual(fi.rem_apos_deducoes_obrigatorias, 1693.24)
        self.assertEqual(fi.vinculo, "ESTATUTARIO")
        self.assertEqual(fi.matricula, "000000000")

        s = '12/2019 (COMP);AGEPREV;INATIVO - APOSENTADO;ALONZO CHURCH;123.***.***-123;AUXILIAR DE PROVAS AUTOMATICAS DE TEOREMAS;"1493,24";"200,00";"1693,24";ESTATUTARIO;000000000'
        fi = folhams._FolhaItem(s)
        comp = folhams._Competencia('12', '2019', 'COMP')
        self.assertEqual(fi.competencia.mes, comp.mes)
        self.assertEqual(fi.competencia.ano, comp.ano)
        self.assertEqual(fi.competencia.tipo, comp.tipo)

        s = '05/2017 (13º);AGEPREV;INATIVO - APOSENTADO;ALONZO CHURCH;123.***.***-123;AUXILIAR DE PROVAS AUTOMATICAS DE TEOREMAS;"1493,24";"200,00";"1693,24";ESTATUTARIO;000000000'
        fi = folhams._FolhaItem(s)
        comp = folhams._Competencia('05', '2017', '13')
        self.assertEqual(fi.competencia.mes, comp.mes)
        self.assertEqual(fi.competencia.ano, comp.ano)
        self.assertEqual(fi.competencia.tipo, comp.tipo)

    def test_Folha(self):

        data = ['01/2018;AGEPREV;INATIVO - APOSENTADO;ALONZO CHURCH;123.***.***-123;AUXILIAR DE PROVAS AUTOMATICAS DE TEOREMAS;"1493,24";"200,00";"1693,24";ESTATUTARIO;000000000',
                '12/2019 (COMP);SED;ATIVO;JOHN VON NEUMANN;123.***.***-123;GRANDE MATEMÁTICO;"1493,24";"200,00";"1693,24";COMISSIONADO REGIME GERAL;000000000',
                '05/2017 (13º);SAD;INATIVO - PENSÃO POR MORTE;KURT GODEL;123.***.***-123;ASSISTENTE DE INCOMPLETUDE;"1493,24";"200,00";"1693,24";MAGISTÉRIO CONVOCADO;000000000'
                ]
        folha = folhams._Folha(data)
        self.assertEqual(len(folha), 3)
        self.assertEqual(folha.itens[0].nome, "ALONZO CHURCH")
        self.assertEqual(folha.itens[1].nome, "JOHN VON NEUMANN")
        self.assertEqual(folha.itens[2].nome, "KURT GODEL")

        self.assertEqual(folha.filter_nome("KURT GODEL")[0].nome, "KURT GODEL")
        self.assertEqual(len(folha.filter_nome("KURT GODEL")), 1)

        self.assertEqual(len(folha.filter_nome("GOKU")), 0)

        self.assertEqual(folha.filter_orgao("AGEPREV")
                         [0].nome, "ALONZO CHURCH")
        self.assertEqual(len(folha.filter_orgao("AGEPREV")), 1)

        self.assertEqual(folha.filter_cargo(
            "ASSISTENTE DE INCOMPLETUDE")[0].nome, "KURT GODEL")
        self.assertEqual(len(folha.filter_cargo(
            "ASSISTENTE DE INCOMPLETUDE")), 1)

        self.assertEqual(folha.filter_situacao("ATIVO")
                         [0].nome, "JOHN VON NEUMANN")
        self.assertEqual(len(folha.filter_situacao("ATIVO")), 1)

        self.assertEqual(folha.filter_vinculo(
            "MAGISTÉRIO CONVOCADO")[0].nome, "KURT GODEL")
        self.assertEqual(len(folha.filter_vinculo("MAGISTÉRIO CONVOCADO")), 1)

    def test_Arquivo(self):

        data = ['[cabeçalho]\n',
                '01/2018;AGEPREV;INATIVO - APOSENTADO;ALONZO CHURCH;123.***.***-123;AUXILIAR DE PROVAS AUTOMATICAS DE TEOREMAS;"1493,24";"200,00";"1693,24";ESTATUTARIO;000000000\n',
                '12/2019 (COMP);SED;ATIVO;JOHN VON NEUMANN;123.***.***-123;GRANDE MATEMÁTICO;"1493,24";"200,00";"1693,24";COMISSIONADO REGIME GERAL;000000000\n',
                '05/2017 (13º);SAD;INATIVO - PENSÃO POR MORTE;KURT GODEL;123.***.***-123;ASSISTENTE DE INCOMPLETUDE;"1493,24";"200,00";"1693,24";MAGISTÉRIO CONVOCADO;000000000'
                ]

        file_test = 'test_read_file.txt'

        with open(file_test, 'w') as f:
            f.writelines(data)

        p = pathlib.Path(file_test)

        arquivo = folhams.Arquivo(p)

        self.assertEqual(arquivo.folha.itens[0].nome, "ALONZO CHURCH")
        self.assertEqual(arquivo.folha.itens[1].nome, "JOHN VON NEUMANN")
        self.assertEqual(arquivo.folha.itens[2].nome, "KURT GODEL")

        self.assertEqual(arquivo.filter_nome(
            "KURT GODEL")[0].nome, "KURT GODEL")
        self.assertEqual(len(arquivo.filter_nome("KURT GODEL")), 1)

        self.assertEqual(len(arquivo.filter_nome("GOKU")), 0)

        self.assertEqual(arquivo.filter_orgao(
            "AGEPREV")[0].nome, "ALONZO CHURCH")
        self.assertEqual(len(arquivo.filter_orgao("AGEPREV")), 1)

        self.assertEqual(arquivo.filter_cargo(
            "ASSISTENTE DE INCOMPLETUDE")[0].nome, "KURT GODEL")
        self.assertEqual(len(arquivo.filter_cargo(
            "ASSISTENTE DE INCOMPLETUDE")), 1)

        self.assertEqual(arquivo.filter_situacao(
            "ATIVO")[0].nome, "JOHN VON NEUMANN")
        self.assertEqual(len(arquivo.filter_situacao("ATIVO")), 1)

        self.assertEqual(arquivo.filter_vinculo(
            "MAGISTÉRIO CONVOCADO")[0].nome, "KURT GODEL")
        self.assertEqual(
            len(arquivo.filter_vinculo("MAGISTÉRIO CONVOCADO")), 1)

        # delete file
        os.remove(file_test)


if __name__ == '__main__':
    unittest.main()
