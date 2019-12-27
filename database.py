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
    python database.py -main -gerar
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

    if '-main' in sys.argv and '-gerar' in sys.argv:
        main()
        tipos = ('orgao', 'situacao', 'cargo', 'vinculo')
        for tipo in tipos:
            create_file(f'{tipo}.csv', folhams.select_tipo(tipo))

        create_file('nome.csv', folhams.select_nome())
    else:
        main()

    print("Concluído!")
    print("*" * 70)
