import os
from datetime import datetime
from typing import List, Set
from pathlib import Path

import requests
import models


__all__ = [
    'url_gov', 'get_online', 'get_page_text', 'link_to_path_files',
    'read_file', 'get_all_files', 'insert_tipo', 'FolhaMS'
]


# [TODO]
###########################################################
#                   scraping web
###########################################################
def url_gov() -> str:
    url = 'http://www.dados.ms.gov.br/dataset/folha-de-pagamento'
    return url


def get_page_text() -> str:
    r = requests.get(url_gov())
    text = r.text
    return text


# [TODO]
def get_online() -> bool:
    return True


###########################################################
#                   manipulate files / dir
###########################################################
def link_to_path_files() -> str:
    """caminho para os arquivos da folha de pagamento (.txt)"""
    path = f'{os.getcwd()}/arquivos/'
    return path


def read_file(file: str) -> List[str]:
    """Retorna arquivo, cada elemento da lista é uma str do arquivo"""
    with open(file) as f:
        data = f.readlines()
    # ignora o cabeçalho do arquivo
    return data[1:]


def get_all_files(path: str = None) -> Set[str]:
    path = path if path else link_to_path_files()
    p = Path(path)
    files = {str(file) for file in p.iterdir() if file.is_file()}
    return files


###########################################################
#                       utils
###########################################################
def str2date(s: str) -> datetime:
    return datetime.strptime(s, '%m-%Y')


def namefromfile(s: str) -> str:
    """ 
    /home/users/folder/folha-09-2019.txt' -> '09-2019'
    'folha-06-2018.txt' -> '06-2018'

    """
    s = s.split("/")[-1]
    s = s.replace("folha-", "")
    s = s.replace(".txt", "")
    return s


def str2float(s: str) -> float:
    s = s.strip('"')
    s = s.strip("'")
    s = s.replace(",", ".")
    return float(s)


###########################################################
#                       db
###########################################################
@models.orm.db_session
def insert_tipo() -> None:
    tipos = models.orm.select(t.descricao for t in models.Tipo).distinct()

    cargo = models.orm.select(i.cargo for i in models.Item
                              if i.cargo not in tipos).distinct()

    vinculo = models.orm.select(i.vinculo for i in models.Item
                                if i.vinculo not in tipos).distinct()

    situacao = models.orm.select(i.situacao for i in models.Item
                                 if i.situacao not in tipos).distinct()

    orgao = models.orm.select(i.orgao for i in models.Item
                              if i.orgao not in tipos).distinct()

    cont = 0
    for i in cargo:
        models.Tipo(tipo='cargo', descricao=i)
        cont += 1
    print('cargo: ', cont)

    cont = 0
    for i in vinculo:
        models.Tipo(tipo='vinculo', descricao=i)
        cont += 1
    print('vinculo: ', cont)

    cont = 0
    for i in situacao:
        models.Tipo(tipo='situacao', descricao=i)
        cont += 1
    print('situacao: ', cont)

    cont = 0
    for i in orgao:
        models.Tipo(tipo='orgao', descricao=i)
        cont += 1
    print('orgao: ', cont)


@models.orm.db_session
def insert_db_itens(folha: models.Folha, file: str) -> int:
    with open(file) as f:
        data = f.readlines()
    for item in data[1:]:
        item = item.strip("\n ")
        item = item.split(";")
        itemmod = models.Item(folha=folha,
                              competencia=item[0],
                              orgao=item[1],
                              situacao=item[2],
                              nome=item[3],
                              cargo=item[5],
                              remuneracao_base=str2float(item[6]),
                              outras_verbas=str2float(item[7]),
                              remuneracao_apos_deducoes_obrigatorias=str2float(
                                  item[8]),
                              vinculo=item[9],
                              matricula=item[10])
    return len(data[1:])


@models.orm.db_session
def init_db(files: Set[str]) -> None:

    f = set(models.orm.select(f.link for f in models.Folha))
    files = files - f

    for file in files:
        print("inserindo file: ", file)
        folha = models.Folha(arquivo_nome=namefromfile(file),
                             quantidade_registros=0,
                             link=file,
                             gerado_analise=False)
        qnt = insert_db_itens(folha, file)
        print("itens inseridos: ", qnt)
        folha.quantidade_registros = qnt
        models.db.commit()


# @models.orm.db_session
# def analise() -> None:
#     folhas = models.orm.select(f for f in models.Folha if not f.gerado_analise)
#     for folha in folhas:
#         itens = models.orm.select(i for i in models.Item if i.folha == folha)

#         print(folha.link, ' - ', len(itens))


class FolhaMS:
    def __init__(self):
        self._query = None
        self.res = {
            'media_rem_base': 0.0,
            'media_outras_verbas': 0.0,
            'media_rem_apos': 0.0,
            'soma_rem_base': 0.0,
            'soma_outras_verbas': 0.0,
            'soma_rem_apos': 0.0
        }

    def select(self, query) -> None:

        # [TODO] insert here 
        keys = ('cargo', 'situacao', 'orgao', 
        'competencia', 'nome', 'vinculo', 'matricula')

        if any((i for i in query.keys() if i not in keys)):
            raise AttributeError('param sql invalid ')

        nova_query = ''

        for k, v in query.items():
            if v:
                nova_query += f' i.{k} == "{v}" and'

        nova_query = nova_query.rstrip(' and')
        sql = ' select i.id, i.remuneracao_base, i.outras_verbas,  '
        sql += 'i.remuneracao_apos_deducoes_obrigatorias from item i '
        sql += f'where ({nova_query})'
        self._query = sql


    def execute(self) -> None:
        with models.orm.db_session:
            itens = models.Item.select_by_sql(self._query)
        
        if qnt := len(itens):
            s = sum([item.remuneracao_base for item in itens])
            self.res['soma_rem_base'] = s
            self.res['media_rem_base'] = s/qnt

            s = sum([item.outras_verbas for item in itens])
            self.res['soma_outras_verbas'] = s
            self.res['media_outras_verbas'] = s/qnt

            s = sum([item.remuneracao_apos_deducoes_obrigatorias for item in itens])
            self.res['soma_rem_apos'] = s
            self.res['media_rem_apos'] = s/qnt
        else:
            self.res = {
            'media_rem_base': 0.0,
            'media_outras_verbas': 0.0,
            'media_rem_apos': 0.0,
            'soma_rem_base': 0.0,
            'soma_outras_verbas': 0.0,
            'soma_rem_apos': 0.0
        }