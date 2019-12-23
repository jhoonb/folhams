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


if __name__ == '__main__':

    print("*" * 70)
    print("".join([
        "\nAnálise da folha de pagamento do ",
        "Estado do Mato Grosso do Sul\n",
        "Buscando arquivos da folha de pagamento ",
        "do Estado no armazenamento local...\n",
        f"Local padrão: {folhams.link_to_path_files()}"
    ]))

    print("*" * 70)

    main()

    print("Concluído!")
    print("*" * 70)
