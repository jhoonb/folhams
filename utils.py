# .  Copyright (C) 2020   Jhonathan P. Banczek (jpbanczek@gmail.com)
#

import os
import pathlib
import datetime
from typing import List, Tuple

__all__ = ["str2float", "namefile2date", "date2filename", "format_file", "all_files"]


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


def _format_item(item: str) -> Tuple:
    """[summary] transforma uma str em uma tupla válida
    ex. entrada: 
    "12/2012;orgao2;situacao2;nome2;cpf2;cargo2;12,2;1002,2;2002,32;vinculo2;matricula2"
    saída:
    ('12/2012', 'orgao2', 'situacao', ...) 
    
    Arguments:
        item {str} -- ex.: 'a;b;c;d;e;f...'
    
    Returns:
        Tuple -- tupla no formato válido
    """
    item = item.split(";")

    competencia = item[0]
    orgao = item[1]
    situacao = item[2]
    nome = item[3]
    cpf = item[4]
    cargo = item[5]
    # converte os campos númericos
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


def format_file(file):
    file = [_format_item(i) for i in file]
    return file


def read_file(file: str) -> List[str]:
    """Retorna arquivo, cada elemento da 
    lista é uma str do arquivo

    Arguments:
        file {str} -- caminho para o arquivo

    Returns:
        List[str] -- conteúdo do arquivo
    """
    with open(file) as f:
        data = f.readlines()
    # ignora o cabeçalho do arquivo
    return data[1:]


def all_files(path: str = None) -> List[str]:
    """[summary] Retorna todos os arquivos presentes no diretório 'path'

    Keyword Arguments:
        path {str} -- caminho para o diretório (default: {None})

    Returns:
        List[str] -- lista com os arquivos do diretório
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
