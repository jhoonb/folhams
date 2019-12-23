import os
import unittest
import requests
import folhams
from datetime import datetime


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

        data = folhams.read_file(file_test)
        # delete file
        os.remove(file_test)
        self.assertEqual(data, ["read_file_test"])

    def test_get_all_files(self):
        pass


class TestUtils(unittest.TestCase):
    def test_str2float(self):
        self.assertEqual(folhams._str2float("'200,50'"), 200.50)
        self.assertEqual(folhams._str2float('"200,50"'), 200.50)
        self.assertEqual(folhams._str2float("'23,58'"), 23.58)
        self.assertEqual(folhams._str2float('"23,58"'), 23.58)
        self.assertEqual(folhams._str2float("'10000000,58'"), 10000000.58)
        self.assertEqual(folhams._str2float('"10000000,58"'), 10000000.58)

    def test_namefromfile(self):
        dt1 = folhams.namefromfile("folha-06-2019.txt")
        dt2 = folhams.namefromfile("folha-05-2020.txt")
        dt3 = folhams.namefromfile("/folder/folder2/files/folha-09-2018.txt")
        dt4 = folhams.namefromfile("folder/folder2/files/folha-03-2016.txt")
        self.assertEqual(dt1, '06-2019')
        self.assertEqual(dt2, '05-2020')
        self.assertEqual(dt3, '09-2018')
        self.assertEqual(dt4, '03-2016')

    def test_str2date(self):

        dt1 = folhams.str2date("06-2019")
        dt2 = folhams.str2date("05-2020")
        ddt1 = datetime.strptime(folhams.namefromfile("folha-06-2019.txt"),
                                 '%m-%Y')
        ddt2 = datetime.strptime(
            folhams.namefromfile("folder/folder2/files/folha-05-2020.txt"),
            '%m-%Y')
        self.assertEqual(dt1, ddt1)
        self.assertEqual(dt2, ddt2)
        self.assertGreater(dt2, ddt1)
        self.assertLess(dt1, ddt2)


if __name__ == '__main__':
    unittest.main()
