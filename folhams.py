import os
import itertools
from pathlib import Path
from typing import List
from models import FolhaData

import controllers


def link_to_path_files(folder: str = "/arquivos/") -> str:
    """caminho para os arquivos da folha de pagamento (.txt)"""
    path = f'{os.getcwd()}{folder}'
    return path


def get_files_name() -> List[str]:
    p = Path(link_to_path_files())
    files_name = [i.name for i in p.iterdir() if i.is_file()]
    return files_name


def read_file(file_name: str) -> List[str]:
    """Retorna arquivo, cada elemento da lista é uma str do arquivo"""

    path_file = f'{link_to_path_files()}{file_name}'
    with open(path_file, 'r') as file:
        arquivo = file.readlines()
    return arquivo


def read_all_files(files_name: str) -> List[List[str]]:
    arquivos = [read_file(file_name) for file_name in files_name]
    return arquivos


def get_files_online() -> None:
    # [TODO]
    pass


def update_database(online: bool = False) -> bool:

    arquivos_db = controllers.select_arquivo()
    # [TODO] 
    if online:
        pass
        #files_online = get_files_online()
    local_files_name = get_files_name()
    # mantem na lista só os arquivos
    # que não estão no banco de dados
    local_files_name = [i for i in local_files_name if i not in arquivos_db]
    files = read_all_files(local_files_name)

    print("".join(["Folhas de pagamentos para analisar e/ou ",
                   f"inserir: {len(files)}"]))

    print("*" * 70)

    if not files:
        return False

    # insere na tabela folha
    for i, arquivo in enumerate(files):
        print(f"Analisando e inserindo {len(arquivo)-1} registros")
        # insert na tabela folha
        folha_data = FolhaData(local_files_name[i])
        folha_data.append(arquivo)
        quantidade = len(folha_data)

        controllers.insert_folha(folha_data)

        print(f"{quantidade} registros inseridos na tabela Folha")

        # insert na tabela Arquivo
        controllers.insert_arquivo(folha_data.name_file, quantidade)
        print(f"Inserida a folha: {folha_data.name_file}")
    
    return True


def gerar_analise(tipo):

    meses = ('01', '02', '03', '04', '05', '06', '07',
             '08', '09', '10', '11', '12')

    # [TODO] inserir na tupla anos, os próximos anos para análise.
    anos = ('2018', '2019')

    # gera com as combinacoes de folha com decimo terceiro e/ou complementar
    for decimo_terceiro, complementar in \
            itertools.product((True, False), repeat=2):

        print(f"Decimo terceiro: {decimo_terceiro}"
              f"| complementar: {complementar}")

        for ano in anos:
            print(f"tipo: {tipo}")
            for mes in meses:
                print(f"ANO: {ano} | MES: {mes}")
                controllers.analise(tipo, ano, mes,
                                    complementar, decimo_terceiro)


def main() -> None:
    # [TODO] se tiver algum outro tipo para a query, inserir.
    tipos = (
        'orgao', 'vinculo',
        'cargo', 'situacao'
    )
    # atualizar
    if not update_database():
        return 

    for tipo in tipos:
        gerar_analise(tipo)


if __name__ == '__main__':

    print("*" * 70)
    print("".join(["\nAnálise da folha de pagamento do ",
                   "Estado do Mato Grosso do Sul\n",
                   "Buscando arquivos da folha de pagamento ",
                   "do Estado no armazenamento local...\n",
                   f"Local padrão: {link_to_path_files()}"]))

    print("*" * 70)
    main()

    print("Concluído!")
    print("*" * 70)
