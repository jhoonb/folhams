import os
from pony.orm import *

_caminho_bd = os.getcwd() + "/bd_folha.sqlite"

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

"""
class AnaliseOrgao(db.Entity):
    codigo = PrimaryKey(int, auto=True)
    orgao = Required(str)
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


class AnaliseCargo(db.Entity):
    codigo = PrimaryKey(int, auto=True)
    cargo = Required(str)
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


class AnaliseVinculo(db.Entity):
    codigo = PrimaryKey(int, auto=True)
    vinculo = Required(str)
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
"""


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