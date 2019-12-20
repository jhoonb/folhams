import os
import shelve
from typing import List
from dataclasses import dataclass
from pathlib import Path, PosixPath

import requests

__all__ = ['url_gov',
           'get_online',
           'get_page_text',
           'link_to_path_files',
           'read_file',
           'get_all_files',
           'Arquivo'
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


def read_file(file: PosixPath) -> List[str]:
    """Retorna arquivo, cada elemento da lista é uma str do arquivo"""
    with file.open() as f:
        data = f.readlines()
    # ignora o cabeçalho do arquivo
    return data[1:]


def get_all_files() -> List[PosixPath]:
    p = Path(link_to_path_files())
    files = [file for file in p.iterdir() if file.is_file()]
    return files


###########################################################
#                       models data
###########################################################
def _str2float(s: str) -> float:
    s = s.strip('"')
    s = s.strip("'")
    s = s.replace(",", ".")
    return float(s)


@dataclass
class _Competencia:
    mes: str
    ano: str
    tipo: str  # 'COMP' -> Complementar | '13' -> décimo 13º | '' -> nenhum


class _FolhaItem:

    def __init__(self, item: str) -> None:

        item = item.strip("\n ")
        item = item.split(";")
        if len(item) != 11:
            raise ValueError(f"item com valor formato inválido: {item}")

        self.competencia = self._competencia(item[0])
        self.orgao = item[1]
        self.situacao = item[2]
        self.nome = item[3]
        self.cpf = item[4]
        self.cargo = item[5]
        self.rem_base = _str2float(item[6])
        self.outras_verbas = _str2float(item[7])
        self.rem_apos_deducoes_obrigatorias = _str2float(item[8])
        self.vinculo = item[9]
        self.matricula = item[10]

    def _competencia(self, valor) -> _Competencia:
        '''
        '12/2018 (13º)' -> Competencia('12', '2018', '13')
        '12/2018 (COMP)' -> Competencia('12', '2018', 'COMP')
        '12/2018' -> Competencia('12', '2018', '')
        '''
        mes, ano = valor.split("/")
        ano = ano[:4]

        if 'COMP' in valor:
            return _Competencia(mes, ano, 'COMP')
        elif '13º' in valor:
            return _Competencia(mes, ano, '13')
        else:
            return _Competencia(mes, ano, '')


class _Folha:

    def __init__(self, data: List[str]) -> None:
        self.itens = []
        self._insert(data)

    def _insert(self, data) -> None:
        for item in data:
            folha_item = _FolhaItem(item)
            self.itens.append(folha_item)

    def __len__(self):
        return len(self.itens)

    def filter_nome(self, nome: str) -> List[_FolhaItem]:
        itens = [item for item in self.itens if nome == item.nome]
        return itens

    def filter_orgao(self, orgao: str) -> List[_FolhaItem]:
        itens = [item for item in self.itens if orgao == item.orgao]
        return itens

    def filter_situacao(self, situacao: str) -> List[_FolhaItem]:
        itens = [item for item in self.itens if situacao == item.situacao]
        return itens

    def filter_cargo(self, cargo: str) -> List[_FolhaItem]:
        itens = [item for item in self.itens if cargo == item.cargo]
        return itens

    def filter_vinculo(self, vinculo: str) -> List[_FolhaItem]:
        itens = [item for item in self.itens if vinculo == item.vinculo]
        return itens


class Arquivo:

    def __init__(self, file: PosixPath):
        self.descricao = file.name
        data = read_file(file)
        self.folha = _Folha(data)
        data = None

    def filter_nome(self, nome: str) -> List[_FolhaItem]:
        return self.folha.filter_nome(nome)

    def filter_orgao(self, orgao: str) -> List[_FolhaItem]:
        return self.folha.filter_orgao(orgao)

    def filter_situacao(self, situacao: str):
        return self.folha.filter_situacao(situacao)

    def filter_cargo(self, cargo: str) -> List[_FolhaItem]:
        return self.folha.filter_cargo(cargo)

    def filter_vinculo(self, vinculo: str) -> List[_FolhaItem]:
        return self.folha.filter_vinculo(vinculo)


@dataclass
class Analise:
    tipo: str
    descricao: str
    competencia: _Competencia
    media_remuneracao_base: float
    media_outras_verbas: float
    media_remuneracao_apos_deducoes: float
    somatorio_remuneracao_base: float
    somatorio_outras_verbas: float
    somatorio_remuneracao_apos_deducoes: float

###########################################################
#                       análises
###########################################################


def gerar_analise(itens: List[_FolhaItem]) -> Analise:

    s_rem_base = 0
    s_outras_verbas = 0
    s_rem_apos_deducoes = 0

    for item in itens:
        s_rem_base += item.rem_base
        s_outras_verbas += item.outras_verbas
        s_rem_apos_deducoes += item.rem_apos_deducoes_obrigatorias
    else:
        raise ValueError(f"sem itens para análise: {itens}")

    m_rem_base = s_rem_base / len(itens)
    m_outras_verbas = s_outras_verbas / len(itens)
    m_rem_apos_deducoes = s_rem_apos_deducoes / len(itens)
    return Analise('',
                   '',
                   '',
                   m_rem_base,
                   m_outras_verbas,
                   m_rem_apos_deducoes,
                   s_rem_base,
                   s_outras_verbas,
                   s_rem_apos_deducoes)


def analisar_por_tipo(arquivo: Arquivo, tipo: str) -> Analise:
    print(arquivo.descricao)
    print(len(arquivo.folha))
    if tipo == 'cargo':
        analise = gerar_analise(arquivo.filter_cargo(tipo))
    elif tipo == 'orgao':
        analise = gerar_analise(arquivo.filter_orgao(tipo))
    elif tipo == 'vinculo':
        analise = gerar_analise(arquivo.filter_vinculo(tipo))
    elif tipo == 'situacao':
        analise = gerar_analise(arquivo.filter_situacao(tipo))
    else:
        raise AttributeError(f"tipo {tipo} Não definido")
    analise.tipo = tipo
    return analise


def create_database(files: List[PosixPath]) -> None:

    with shelve.open('database.shelve') as db:

        # insere apenas os que faltam
        files = [file for file in files
                 if file.name not in db.keys()]

        for file in files:
            print(f"arquivo: {file.name}")
            arquivo = Arquivo(file)
            db[arquivo.descricao] = arquivo
            # db.sync()
        else:
            print('Nenhum arquivo para inserir')


def check_database_analise() -> bool:
    with shelve.open('analise.shelve') as db_analise:
        valor = db_analise.get("tipos", None)
    return True if valor else False


def create_database_analise() -> None:

    # [TODO]
    if not check_database_analise():
        tipos = {
            'orgao', 'vinculo',
            'cargo', 'situacao'
        }

    with shelve.open('database.shelve') as db:

        with shelve.open('analise.shelve') as db_analise:
            for k, arquivo in db.items():
                ktipos = {}
                for tipo in tipos:
                    dados = analisar_por_tipo(arquivo, tipo)
                    ktipos[tipo] = dados
                db_analise[k] = ktipos
                db[arquivo.descricao] = arquivo
                # db.sync()
