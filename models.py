import os
from typing import List

from pony.orm import *


_caminho_bd = f"{os.getcwd()}/bd_folha.sqlite"


db = Database("sqlite", _caminho_bd, create_db=True)


class Arquivo(db.Entity):
    codigo = PrimaryKey(int, auto=True)
    arquivo_nome = Required(str)
    quantidade_registros = Required(int)


class Folha(db.Entity):
    codigo = PrimaryKey(int, auto=True)
    competencia_ano = Required(str)
    competencia_mes = Required(str)
    orgao = Required(str)
    situacao = Required(str)
    nome = Required(str)
    cpf = Required(str)
    cargo = Required(str)
    remuneracao_base = Required(float)
    outras_verbas = Required(float)
    remuneracao_apos_deducoes_obrigatorias = Required(float)
    vinculo = Required(str)
    matricula = Required(str)
    complementar = Required(bool)
    decimo_terceiro = Required(bool)


class Analise(db.Entity):
    codigo = PrimaryKey(int, auto=True)
    tipo = Required(str)
    descricao = Required(str)
    competencia_ano = Required(str)
    competencia_mes = Required(str)
    media_remuneracao_base = Required(float)
    media_outras_verbas = Required(float)
    media_remuneracao_apos_deducoes = Required(float)
    somatorio_remuneracao_base = Required(float)
    somatorio_outras_verbas = Required(float)
    somatorio_remuneracao_apos_deducoes = Required(float)
    complementar = Required(bool)
    decimo_terceiro = Required(bool)


class Controle(db.Entity):
    codigo = PrimaryKey(int, auto=True)
    tipo = Required(str)
    competencia_ano = Required(str)
    competencia_mes = Required(str)
    complementar = Required(bool)
    decimo_terceiro = Required(bool)


db.generate_mapping(create_tables=True)


######################################################
# Objetos para mapear
#######################################################
class FolhaLinha:
    def __init__(self, data):
        _data = data.split(";")
        _mes, _ano = _data[0].split("/")

        self.competencia_mes = _mes
        self.competencia_ano = _ano[:4]
        self.orgao = _data[1]
        self.situacao = _data[2]
        self.nome = _data[3]
        self.cpf = _data[4]
        self.cargo = _data[5]
        self.base = self._str_to_float(_data[6])
        self.outras = self._str_to_float(_data[7])
        self.apos = self._str_to_float(_data[8])
        self.vinculo = _data[9]
        self.matricula = _data[10]
        self.complementar = self._complementar(_ano[4:])
        self.decimo_terceiro = self._decimo_terceiro(_ano[4:])

    def _complementar(self, s: str) -> bool:
        """Retorna True se for folha entrada complementar"""
        return True if 'COMP' in s else False

    def _decimo_terceiro(self, s: str) -> bool:
        """Retorna True se for folha de 13º salário"""
        return True if '13' in s else False

    def _str_to_float(self, s: str) -> float:
        """Converte str para float, ex.: formato '30,5' para float 30.5"""
        s = s.replace('"', '')
        s = s.replace(',', '.')
        return float(s)


class FolhaData:
    def __init__(self, name_file: str):
        self.name_file = name_file
        self.linhas = []

    def append(self, arquivo: List[str]) -> None:
        for data in arquivo:
            self.linhas.append(FolhaLinha(data))

    def __len__(self):
        return len(self.linhas)


class AnaliseData:
    def __init__(self):
        pass
