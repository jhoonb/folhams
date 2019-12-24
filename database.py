import sys
import folhams

def main() -> None:

    # folhams.get_online()
    files = folhams.get_all_files()
    print(f"arquivos na pasta: {len(files)} arquivo(s)")
    print("Inserindo dados no Banco de dados sqlite: ")
    folhams.init_db(files)
    print("insertindo tabela tipo: ")
    folhams.insert_tipo()
    #folhams.analise()
    print("Encerrado")


def create_file(file_name, data):
    with open(file_name, 'w') as f:
        for d in data:
            f.write("|" + d)
            f.write("\n")


if __name__ == '__main__':
    """
    python database.py 
    python database.py - main
    python database.py -main -arquivos-tipos
    """

    print("*" * 70)
    print("".join([
        "\nAnálise da folha de pagamento do ",
        "Estado do Mato Grosso do Sul\n",
        "Buscando arquivos da folha de pagamento ",
        "do Estado no armazenamento local...\n",
        f"Local padrão: {folhams.link_to_path_files()}"
    ]))

    print("*" * 70)

    if '-main' in sys.argv and '-arquivos-tipos' in sys.argv:
        main()
        create_file('orgao.txt', folhams.select_orgao())
        create_file('situacao.txt', folhams.select_situacao())
        create_file('cargo.txt', folhams.select_cargo())
        create_file('vinculo.txt', folhams.select_vinculo())
        create_file('nome.txt', folhams.select_nome())
    else:
        main()

    print("Concluído!")
    print("*" * 70)
