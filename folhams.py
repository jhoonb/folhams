# .  Copyright (C) 2020   Jhonathan P. Banczek (jpbanczek@gmail.com)
#

import sys
import os
import hashlib
import pathlib
import datetime
from typing import List, Dict, Set, Tuple

import models


def str2float(s: str) -> float:
    """ Converte o valor str (do arquivo .txt) para float

    Arguments:
        s {str} -- str no formato, ex.: '23,4'

    Returns:
        float -- 23.4
    """
    s = s.strip('"')
    s = s.strip("'")
    s = s.replace(",", ".")
    return float(s)


def namefile2date(s: str) -> datetime.datetime:
    """converte a str s para tipo datetime

    Arguments:
        s {str} -- data: path/path/.../path/folha-01-2000.txt

    Returns:
        datetime -- mm-YYYY: 01-2000 
    """
    s = s.split("/")[-1]
    s = s.replace("folha-", "")
    s = s.replace(".txt", "")
    s = s.strip()
    return datetime.datetime.strptime(s, "%m-%Y")


def date2filename(dt: datetime.datetime, path: str) -> str:
    """[summary] converte a data dt para caminho do arquivo
    
    Arguments:
        dt {datetime.datetime} -- formato ex. datetime.datetime(2020, 2, 1, 0, 0)
        path {str} -- ex.: /path/to/file/
    
    Returns:
        str -- ex.: /path/to/file/folha-02-2020.txt
    """
    # 2018-10-01 00:00:00
    file = "{}/folha-{}-{}.txt"
    s = str(dt)
    s = s.split(" ")[0]
    s = s.split("-")
    file = file.format(path, s[1], s[0])
    file = file.replace("//", "/")
    return file


def format_item(item: str) -> Tuple:
    item = item.split(";")

    competencia = item[0]
    orgao = item[1]
    situacao = item[2]
    nome = item[3]
    cpf = item[4]
    cargo = item[5]
    rem_base = str2float(item[6])
    outras_verbas = str2float(item[7])
    rem_posdeducoes = str2float(item[8])
    vinculo = item[9]
    matricula = item[10]

    return (
        competencia,
        orgao,
        situacao,
        nome,
        cpf,
        cargo,
        rem_base,
        outras_verbas,
        rem_posdeducoes,
        vinculo,
        matricula,
    )


# ok
def format_file(file):
    file = [format_item(i) for i in file]
    return file


# ok
def read_file(file: str) -> List[str]:
    """Retorna arquivo, cada elemento da 
    lista é uma str do arquivo

    Arguments:
        file {str} -- [description]

    Returns:
        List[str] -- [description]
    """
    with open(file) as f:
        data = f.readlines()
    # ignora o cabeçalho do arquivo
    return data[1:]


# ok
def all_files(path: str = None) -> List[str]:
    """[summary]

    Keyword Arguments:
        path {str} -- [description] (default: {None})

    Returns:
        Set[str] -- [description]
    """
    path = f"{os.getcwd()}/arquivos/" if not path else path
    p = pathlib.Path(path)
    # folhas (sem 13º)
    files = {
        namefile2date(str(f)) for f in p.iterdir() if f.is_file() and not "13" in f.stem
    }
    # ordenar os arquivos por data
    files = sorted(files)
    files = [date2filename(f, path) for f in files]
    # folha apenas do 13º
    files13 = [str(f) for f in p.iterdir() if f.is_file() and "13" in f.stem]
    # une as duas folhas
    files.extend(files13)
    return files


# ok
def db_all_files():
    arquivo = models.Arquivo()
    fields = "descricao"
    params = "WHERE 1"
    dados = arquivo.select(fields, params)
    dados = [i[0] for i in dados]
    arquivo.close()
    return dados


# ok
def get_new_files():
    # lista de arquivos local
    arquivos = all_files()
    # arquivos inseridos no banco
    arquivos_db = db_all_files()
    # apenas arquivos que não foram inseridos
    arquivos = [f for f in arquivos if not f.split("/")[-1] in arquivos_db]
    print("quantidade de folhas a inserir:", len(arquivos))
    return arquivos


# ok
def atualizar_banco() -> None:
    arquivos = get_new_files()
    # insere arquivo e folha no banco de dados
    quantidades = []

    folhadb = models.Folha()

    for arq in arquivos:
        print(f"inserindo folha: {arq}")
        file = read_file(arq)
        folha = format_file(file)
        folhadb.insert(folha)
        quantidades.append(len(folha))

    folhadb.close()

    if arquivos:
        arquivodb = models.Arquivo()
        # apenas nome do arquivo
        arquivos = [i.split("/")[-1] for i in arquivos]
        arquivos = list(zip(arquivos, quantidades))
        arquivodb.insert(arquivos)
        arquivodb.close()


def db_all_orgao(competencia):
    folhadb = models.Folha()
    fields = "DISTINCT orgao"
    params = f'WHERE competencia like "{competencia}"'
    orgaos = folhadb.select(fields, params)
    orgaos = [i[0] for i in orgaos]
    folhadb.close()
    return orgaos


def db_maior_salario(
    competencia, quantidade=50, remuneracao_por="rem_posdeducoes"
) -> int:
    orgaos = db_all_orgao(competencia)
    if not orgaos:
        return 0

    ids = []
    fields = "id"
    query = "{};{};{};{}"

    folhadb = models.Folha()
    for orgao in orgaos:
        params = f"""WHERE competencia like "{competencia}" and 
        orgao like "{orgao}" 
        ORDER BY {remuneracao_por} 
        DESC LIMIT {quantidade}"""
        data = folhadb.select(fields, params)
        data = ";".join([str(i[0]) for i in data])
        ids.append((query.format(fields, competencia, orgao, quantidade), data))
    folhadb.close()
    # from pprint import pprint
    # pprint(ids)
    consultadb = models.Consulta()
    fields = "query"
    params = "WHERE 1"

    inseridos = [i[0] for i in consultadb.select(fields, params)]
    # apenas os que nao foram inseridos no banco
    ids = [i for i in ids if i[0] not in inseridos]

    print(consultadb)
    consultadb.insert(ids)
    consultadb.close()
    return len(ids)

# [TODO] outras opcoes
if __name__ == "__main__":
    arg = None if len(sys.argv) <= 1 else sys.argv[1]
    if arg == "update":
        atualizar_banco()
    else:
        print("""
        FolhaMS - Folha de Pagamento do MS
        Parametros
        Para inserir os dados da folha no banco:
        ----------------------------------------
        python folhams.py update 
        """)
