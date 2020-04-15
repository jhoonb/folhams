# .  Copyright (C) 2020   Jhonathan P. Banczek (jpbanczek@gmail.com)
#

import sys

import models
import utils
from typing import List, Tuple


def db_all_files() -> List[str]:
    arquivo = models.Arquivo()
    fields = "descricao"
    params = "WHERE 1"
    dados = arquivo.select(fields, params)
    # apenas campo descricao
    dados = [i[0] for i in dados]
    arquivo.close()
    return dados


def get_new_files() -> List[str]:
    # lista de arquivos local
    arquivos = utils.all_files()
    # arquivos inseridos no banco
    arquivos_db = db_all_files()
    # apenas arquivos que não foram inseridos
    arquivos = [f for f in arquivos if not f.split("/")[-1] in arquivos_db]
    print("quantidade de folhas a inserir:", len(arquivos))
    return arquivos


def atualizar_banco() -> None:
    if not (arquivos := get_new_files()):
        return

    # insere arquivo e folha no banco de dados
    folhadb = models.Folha()
    arquivodb = models.Arquivo()

    for arq in arquivos:
        print(f"inserindo folha: {arq}")
        file = utils.read_file(arq)
        folha = utils.format_file(file)
        itens = len(folha)
        data = [(arq.split("/")[-1], itens)]
        id_arquivo = arquivodb.insert(data)
        folha = [list(i) + [id_arquivo] for i in folha]
        # from pprint import pprint
        # pprint(folha)
        folhadb.insert(folha)

    folhadb.close()
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
    query = "{};{};{};{};{}"

    folhadb = models.Folha()
    for orgao in orgaos:
        params = f"""WHERE competencia like "{competencia}" and 
        orgao like "{orgao}" 
        ORDER BY {remuneracao_por} 
        DESC LIMIT {quantidade}"""
        data = folhadb.select(fields, params)
        data = ";".join([str(i[0]) for i in data])
        ids.append((
            query.format(fields, 
            competencia, 
            orgao, 
            quantidade, 
            remuneracao_por),
            data,
            False))
    
    folhadb.close()
    consultadb = models.Consulta()

    fields = "query"
    params = "WHERE 1"

    inseridos = [i[0] for i in consultadb.select(fields, params)]
    # apenas os que nao foram inseridos no banco
    ids = [i for i in ids if i[0] not in inseridos]
    if not ids:
        return 0
    idds = consultadb.insert(ids)
    consultadb.close()
    return len(ids)


def gerar_dados():
    consultadb = models.Consulta()
    fields, params = "", ""
    dados_db = consultadb.select()
    consultadb.close()

def criar_banco() -> None:
    a = models.Arquivo()
    f = models.Folha()
    c = models.Consulta()
    a.close()
    f.close()
    c.close()


# [TODO] outras opcoes
if __name__ == "__main__":
    arg = None if len(sys.argv) <= 1 else sys.argv[1]
    if arg == "update":
        # cria a estrutura do banco, se não foi criado
        criar_banco()
        atualizar_banco()
    else:
        print(
            """
        FolhaMS - Folha de Pagamento do MS
        Parametros
        Para inserir os dados da folha no banco:
        ----------------------------------------
        python folhams.py update 
        """
        )
        criar_banco()
        atualizar_banco()
