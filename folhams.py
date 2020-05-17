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
        folhadb.insert(folha)

    folhadb.close()
    arquivodb.close()


def criar_banco() -> None:
    a = models.Arquivo()
    f = models.Folha()
    a.close()
    f.close()


if __name__ == "__main__":
    print(
        """
        FolhaMS - Folha de Pagamento do MS
        Parametros
        Para inserir os dados da folha no banco:
        ----------------------------------------
        python folhams.py 
        """)
    # cria a estrutura do banco, se não foi criado
    criar_banco()
    atualizar_banco()