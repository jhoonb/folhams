import os
import logging
import itertools
from pathlib import Path
import sqlite3
import models

# caminho para os arquivos da folha de pagamento (.txt)
caminho_arquivo = os.getcwd() + "/arquivos/"

# configurar o log
logging.basicConfig(format='folhams -> %(asctime)s: %(message)s', 
    level=logging.DEBUG, 
    datefmt='%d/%m/%Y %I:%M:%S')


def str2float(d):
    """
    str2float exemplo: "34,5" -> 34.5
    tipo: d (str)
    retorno: d (float) 
    """
    d = d.replace('"', '')
    d = d.replace(',', '.')
    return float(d)


def e_complementar(s):
    return True if 'COMP' in s else False


def e_decimo_terceiro(s):
    return True if '13' in s[4:] else False


def arquivo_nome(s):
    """
    arquivo_nomes: retorna apenas o nome+extensão do arquivo
    exemplo: /home/user/folhams/arquivos/folha-01-2018.txt
        -> "folha-01-2018.txt"
    retorno: str 
    """
    return str(s).split("/")[-1]


def buscar_arquivos():
    """
    buscar_arquivos retorna um objeto generator
    com o nome de todos os arquivo dentro do diretorio
    retorno: generator
    """
    p = Path(caminho_arquivo)
    return (arquivo_nome(i) for i in p.iterdir() if i.is_file())


def ler_arquivo(arquivo_nome):
    """
    ler_arquivo retorna todo conteudo do arquivo
    em uma lista, cada linha do arquivo é um list de str
    """
    with open(caminho_arquivo + arquivo_nome, 'r') as f:
        d = f.readlines()
    return d


def todos_os_arquivos(arquivos_local):
    """
    todos_os_arquivos retorna uma lista todos os dados
    obtidos dos arquivos
    retorno: list
    """
    return [ler_arquivo(arquivo_nome) for arquivo_nome in arquivos_local]


@models.db_session
def insert_tabela_folha(dados_folhas):
    """
    insert_tabela_folha insere todos os dicts 
    (no formato feito por tratar_arquivo())
    na tabela do banco 'Folha'
    retorno: quantidade de inserts (int)
    """

    for folha in dados_folhas:
        models.Folha(competencia_mes=folha['competencia-mes'],
            competencia_ano=folha['competencia-ano'],
            orgao=folha['orgao'],
            situacao=folha['situacao'],
            nome=folha['nome'],
            cpf=folha['cpf'],
            cargo=folha['cargo'],
            remuneracao_base=folha['base'],
            outras_verbas=folha['outras'],
            remuneracao_apos_deducoes_obrigatorias=folha['apos'],
            vinculo=folha['vinculo'],
            matricula=folha['matricula'],
            complementar=folha['complementar'],
            decimo_terceiro=folha['decimo_terceiro'])

    return len(dados_folhas)


@models.db_session
def insert_tabela_arquivo(nome, quantidade):
    """
    insert_tabela_arquivo insere
    na tabela do banco 'Arquivo' o nome do
    arquivo e a quantidade de itens inserido em Folha
    """
    models.Arquivo(arquivo_nome=nome, quantidade_registros=quantidade)


def tratar_arquivo(arquivo):
    """
    tratar_arquivo retorna uma lista com elementos do
    tipo dict, cada elemento é uma linha do arquivo
    modelo do dict 
    folha = { 'mes': str,
    'competencia-ano' = str,
    'orgao' = str
    'situacao' = str
    'nome' = str
    'cpf' = str
    'cargo' = str
    'base' = float
    'outras' = float
    'apos' = float
    'vinculo' = str
    'matricula' = str
    'complementar' = bool
    'decimo_terceiro' = bool
    retorno: dados_folhas (list)
    """

    dados_folhas = []
    # ignora cabeçalho do arquivo [1:]
    for linha in arquivo[1:]:

        folha = {}
        s = linha.split(";")
        mes, ano = s[0].split("/")
        folha['competencia-mes'] = mes
        folha['competencia-ano'] = ano[:4]
        folha['orgao'] = s[1]
        folha['situacao'] = s[2]
        folha['nome'] = s[3]
        folha['cpf'] = s[4]
        folha['cargo'] = s[5]
        folha['base'] = str2float(s[6])
        folha['outras'] = str2float(s[7])
        folha['apos'] = str2float(s[8])
        folha['vinculo'] = s[9]
        folha['matricula'] = s[10]
        folha['complementar'] = e_complementar(ano[4:])
        folha['decimo_terceiro'] = e_decimo_terceiro(ano[4:])

        dados_folhas.append(folha)

    return dados_folhas


@models.db_session
def select_tabela_arquivo_nomes():
    """
    select_tabela_arquivo_nomes retorna uma lista contendo
    todos os valores do campo arquivo_nome da tabela Arquivo
    retorno: list
    """
    return list(models.select(c.arquivo_nome for c in models.Arquivo))


def atualizar_db():
    """
    atualizar_db verifica quais arquivos no disco local
    ainda não foram inseridos no banco de dados,
    captura-os, efetua os tratamentos e insere no banco
    """
    arquivos_db = select_tabela_arquivo_nomes()
    arquivos_local = buscar_arquivos()
    arquivos_local = [i for i in arquivos_local if i not in arquivos_db]
    dados_arquivos = todos_os_arquivos(arquivos_local)

    logging.info('Folhas de pagamentos para \
analisar e/ou inserir: {}'.format(len(dados_arquivos)))

    # insere na tabela folha
    for i, arquivo in enumerate(dados_arquivos):
        
        logging.info("Analisando e inserindo {} \
registros... Aguarde".format(len(arquivo[1:])))

        # insert na tebela folha
        qnt = insert_tabela_folha(tratar_arquivo(arquivo))
        
        logging.info("{} registros inseridos na tabela Folha".format(qnt))

        # insert na tabela Arquivo
        insert_tabela_arquivo(arquivos_local[i], qnt)
        logging.info("Inserida a folha: {}".format(arquivos_local[i]))


## analise de dados
@models.db_session
def analise(tipo, ano, mes, complementar, decimo_terceiro):

    # verifica se jã não foi inserido
    v = list(models.select(c.codigo for c in models.Controle 
        if c.tipo == tipo 
        and c.competencia_ano == ano 
        and c.competencia_mes == mes 
        and c.complementar == complementar
        and c.decimo_terceiro == decimo_terceiro))

    # se foi inserido pula...
    if v: return 

    # se for folha de 13º, valida apenas se for mês 12,
    # do contrário não faz query
    if decimo_terceiro == True and mes != '12': return

    # todos os tipos ['orgao', 'vinculo', 'cargo', 'situacao'] - distinct
    tipos = None
    if tipo == 'orgao':
        tipos = list(models.select(f.orgao for f in models.Folha 
            if f.competencia_ano == ano 
            and f.competencia_mes == mes 
            and f.complementar == complementar
            and f.decimo_terceiro == decimo_terceiro))
    elif tipo == 'vinculo':
        tipos = list(models.select(f.vinculo for f in models.Folha 
            if f.competencia_ano == ano 
            and f.competencia_mes == mes 
            and f.complementar == complementar
            and f.decimo_terceiro == decimo_terceiro))
    elif tipo == 'cargo':
        tipos = list(models.select(f.cargo for f in models.Folha 
            if f.competencia_ano == ano 
            and f.competencia_mes == mes 
            and f.complementar == complementar
            and f.decimo_terceiro == decimo_terceiro))
    elif tipo == 'situacao':
        tipos = list(models.select(f.situacao for f in models.Folha 
            if f.competencia_ano == ano 
            and f.competencia_mes == mes 
            and f.complementar == complementar
            and f.decimo_terceiro == decimo_terceiro))
    else:
        logging.info("Tipo {} NÃO IMPLEMENTADO".format(tipo))

    # nao retornou resultado [None] na busca
    if not tipos: return

    for t in tipos:
        logging.info("Consultando e inserindo dados: {}".format(t))

        d = {}
        d['tipo'] = tipo
        d['descricao'] = t

        if tipo == 'orgao':
            d['qnt_registros'] = models.count((f for f in models.Folha 
                if f.orgao == t 
                and f.competencia_ano == ano 
                and f.competencia_mes == mes
                and f.complementar == complementar
                and f.decimo_terceiro == decimo_terceiro), distinct=False)

            d['media_rem_base'] = models.avg((f.remuneracao_base for f in models.Folha 
                if f.orgao == t 
                and f.competencia_ano == ano 
                and f.competencia_mes == mes 
                and f.complementar == complementar 
                and f.decimo_terceiro == decimo_terceiro), distinct=False)

            d['media_outras'] = models.avg((f.outras_verbas for f in models.Folha 
                if f.orgao == t 
                and f.competencia_ano == ano 
                and f.competencia_mes == mes 
                and f.complementar == complementar 
                and f.decimo_terceiro == decimo_terceiro), distinct=False)

            d['media_pos'] = models.avg((f.remuneracao_apos_deducoes_obrigatorias for f in models.Folha 
                if f.orgao == t 
                and f.competencia_ano == ano 
                and f.competencia_mes == mes 
                and f.complementar == complementar 
                and f.decimo_terceiro == decimo_terceiro), distinct=False)

            d['soma_rem_base'] = models.sum((f.remuneracao_base for f in models.Folha 
                if f.orgao == t
                and f.competencia_ano == ano 
                and f.competencia_mes == mes 
                and f.complementar == complementar 
                and f.decimo_terceiro == decimo_terceiro), distinct=False)

            d['soma_outras'] = models.sum((f.outras_verbas for f in models.Folha 
                if f.orgao == t 
                and f.competencia_ano == ano 
                and f.competencia_mes == mes
                and f.complementar == complementar 
                and f.decimo_terceiro == decimo_terceiro), distinct=False)

            d['soma_pos'] = models.sum((f.remuneracao_apos_deducoes_obrigatorias for f in models.Folha 
                if f.orgao == t 
                and f.competencia_ano == ano 
                and f.competencia_mes == mes 
                and f.complementar == complementar 
                and f.decimo_terceiro == decimo_terceiro), distinct=False)

        elif tipo == 'vinculo':
            d['qnt_registros'] = models.count((f for f in models.Folha 
                if f.vinculo == t 
                and f.competencia_ano == ano 
                and f.competencia_mes == mes
                and f.complementar == complementar
                and f.decimo_terceiro == decimo_terceiro), distinct=False)

            d['media_rem_base'] = models.avg((f.remuneracao_base for f in models.Folha 
                if f.vinculo == t 
                and f.competencia_ano == ano 
                and f.competencia_mes == mes 
                and f.complementar == complementar 
                and f.decimo_terceiro == decimo_terceiro), distinct=False)

            d['media_outras'] = models.avg((f.outras_verbas for f in models.Folha 
                if f.vinculo == t 
                and f.competencia_ano == ano 
                and f.competencia_mes == mes 
                and f.complementar == complementar 
                and f.decimo_terceiro == decimo_terceiro), distinct=False)

            d['media_pos'] = models.avg((f.remuneracao_apos_deducoes_obrigatorias for f in models.Folha 
                if f.vinculo == t 
                and f.competencia_ano == ano 
                and f.competencia_mes == mes 
                and f.complementar == complementar 
                and f.decimo_terceiro == decimo_terceiro), distinct=False)

            d['soma_rem_base'] = models.sum((f.remuneracao_base for f in models.Folha 
                if f.vinculo == t
                and f.competencia_ano == ano 
                and f.competencia_mes == mes 
                and f.complementar == complementar 
                and f.decimo_terceiro == decimo_terceiro), distinct=False)

            d['soma_outras'] = models.sum((f.outras_verbas for f in models.Folha 
                if f.vinculo == t 
                and f.competencia_ano == ano 
                and f.competencia_mes == mes
                and f.complementar == complementar 
                and f.decimo_terceiro == decimo_terceiro), distinct=False)

            d['soma_pos'] = models.sum((f.remuneracao_apos_deducoes_obrigatorias for f in models.Folha 
                if f.vinculo == t 
                and f.competencia_ano == ano 
                and f.competencia_mes == mes 
                and f.complementar == complementar 
                and f.decimo_terceiro == decimo_terceiro), distinct=False)

        elif tipo == 'cargo':
            d['qnt_registros'] = models.count((f for f in models.Folha 
                if f.cargo == t 
                and f.competencia_ano == ano 
                and f.competencia_mes == mes
                and f.complementar == complementar
                and f.decimo_terceiro == decimo_terceiro), distinct=False)

            d['media_rem_base'] = models.avg((f.remuneracao_base for f in models.Folha 
                if f.cargo == t 
                and f.competencia_ano == ano 
                and f.competencia_mes == mes 
                and f.complementar == complementar 
                and f.decimo_terceiro == decimo_terceiro), distinct=False)

            d['media_outras'] = models.avg((f.outras_verbas for f in models.Folha 
                if f.cargo == t 
                and f.competencia_ano == ano 
                and f.competencia_mes == mes 
                and f.complementar == complementar 
                and f.decimo_terceiro == decimo_terceiro), distinct=False)

            d['media_pos'] = models.avg((f.remuneracao_apos_deducoes_obrigatorias for f in models.Folha 
                if f.cargo == t 
                and f.competencia_ano == ano 
                and f.competencia_mes == mes 
                and f.complementar == complementar 
                and f.decimo_terceiro == decimo_terceiro), distinct=False)

            d['soma_rem_base'] = models.sum((f.remuneracao_base for f in models.Folha 
                if f.cargo == t
                and f.competencia_ano == ano 
                and f.competencia_mes == mes 
                and f.complementar == complementar 
                and f.decimo_terceiro == decimo_terceiro), distinct=False)

            d['soma_outras'] = models.sum((f.outras_verbas for f in models.Folha 
                if f.cargo == t 
                and f.competencia_ano == ano 
                and f.competencia_mes == mes
                and f.complementar == complementar 
                and f.decimo_terceiro == decimo_terceiro), distinct=False)

            d['soma_pos'] = models.sum((f.remuneracao_apos_deducoes_obrigatorias for f in models.Folha 
                if f.cargo == t 
                and f.competencia_ano == ano 
                and f.competencia_mes == mes 
                and f.complementar == complementar 
                and f.decimo_terceiro == decimo_terceiro), distinct=False)
        
        elif tipo == 'situacao':
            d['qnt_registros'] = models.count((f for f in models.Folha 
                if f.situacao == t 
                and f.competencia_ano == ano 
                and f.competencia_mes == mes
                and f.complementar == complementar
                and f.decimo_terceiro == decimo_terceiro), distinct=False)

            d['media_rem_base'] = models.avg((f.remuneracao_base for f in models.Folha 
                if f.situacao == t 
                and f.competencia_ano == ano 
                and f.competencia_mes == mes 
                and f.complementar == complementar 
                and f.decimo_terceiro == decimo_terceiro), distinct=False)

            d['media_outras'] = models.avg((f.outras_verbas for f in models.Folha 
                if f.situacao == t 
                and f.competencia_ano == ano 
                and f.competencia_mes == mes 
                and f.complementar == complementar 
                and f.decimo_terceiro == decimo_terceiro), distinct=False)

            d['media_pos'] = models.avg((f.remuneracao_apos_deducoes_obrigatorias for f in models.Folha 
                if f.situacao == t 
                and f.competencia_ano == ano 
                and f.competencia_mes == mes 
                and f.complementar == complementar 
                and f.decimo_terceiro == decimo_terceiro), distinct=False)

            d['soma_rem_base'] = models.sum((f.remuneracao_base for f in models.Folha 
                if f.situacao == t
                and f.competencia_ano == ano 
                and f.competencia_mes == mes 
                and f.complementar == complementar 
                and f.decimo_terceiro == decimo_terceiro), distinct=False)

            d['soma_outras'] = models.sum((f.outras_verbas for f in models.Folha 
                if f.situacao == t 
                and f.competencia_ano == ano 
                and f.competencia_mes == mes
                and f.complementar == complementar 
                and f.decimo_terceiro == decimo_terceiro), distinct=False)

            d['soma_pos'] = models.sum((f.remuneracao_apos_deducoes_obrigatorias for f in models.Folha 
                if f.situacao == t 
                and f.competencia_ano == ano 
                and f.competencia_mes == mes 
                and f.complementar == complementar 
                and f.decimo_terceiro == decimo_terceiro), distinct=False)

        else:
            logging.info("Tipo {} NÃO IMPLEMENTADO".format(tipo))

        # testar se não retornou nada
        # insere no banco tabela Analise
        if d['soma_outras'] and d['soma_pos'] and d['soma_rem_base']:
            models.Analise(tipo = d['tipo'],
                descricao = d['descricao'], 
                competencia_ano = ano,
                competencia_mes = mes, 
                media_remuneracao_base = d['media_rem_base'],
                media_outras_verbas = d['media_outras'], 
                media_remuneracao_apos_deducoes = d['media_pos'],
                somatorio_remuneracao_base = d['soma_rem_base'], 
                somatorio_outras_verbas = d['soma_outras'],
                somatorio_remuneracao_apos_deducoes = d['soma_pos'],
                complementar = complementar,
                decimo_terceiro = decimo_terceiro)
        else:
            logging.info("Query SQL Não retornou resultados ")

    # inserir controle
    models.Controle(tipo=tipo,
        competencia_ano = ano,
        competencia_mes = mes,
        complementar = complementar,
        decimo_terceiro = decimo_terceiro)


def gerar_analise(tipo):

    # [TODO] inserir na tupla anos, os próximos anos para análise.
    meses = ('01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12')
    anos = ('2018', '2019')

    # gera com as combinacoes de folha com decimo terceiro e/ou complementar
    for decimo_terceiro, complementar in itertools.product((True, False), repeat=2):
        logging.info("Decimo terceiro: {} | complementar: {}".format(decimo_terceiro, complementar))
        for ano in anos:
            logging.info("tipo: {}".format(tipo))
            for mes in meses:
                logging.info("ANO: {} | MES: {}".format(ano, mes))
                analise(tipo, ano, mes, complementar, decimo_terceiro)


@models.db_session
def gerar_grafico():

    import locale

    query = models.select((a.tipo, a.descricao, 
        a.competencia_ano, 
        a.somatorio_remuneracao_apos_deducoes) for a in models.Analise)


    ativo = sum([i[1] for i in query if i[0] == 'ATIVO'])
    inativo_morte = sum([i[1] for i in query if i[0] == 'INATIVO - PENSÃO POR MORTE'])
    inativo_aposentado = sum([i[1] for i in query if i[0] == 'INATIVO - APOSENTADO'])

    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

    print("ativo: ", locale.currency(ativo, grouping=True, symbol=None))
    print("inativo_morte: ", locale.currency(inativo_morte, grouping=True, symbol=None))
    print("inativo_aposentado", locale.currency(inativo_aposentado, grouping=True, symbol=None))
    print("total inativos: ", locale.currency(inativo_aposentado+inativo_morte, grouping=True, symbol=None)) 

    
    # pie = pygal.Pie()
    # pie.title = 'Situação - total de remuneração em 2018 (todos os orgãos)'
    # # -- loop
    # pie.add(situacao, valor)
    # # --
    # pie.render_to_file('/home/jhoonb/situacao.svg') 

"""
refatorar: 
- gerar_grafico()
- gerar_analise(tipo)
- analise(tipo, ano, mes, complementar, decimo_terceiro)
"""
if __name__ == '__main__':

    logging.info("Análise da folha de pagamento do Estado do Mato Grosso do Sul")    
    logging.info("Buscando arquivos da folha de pagamento do Estado no armazenamento local...")
    logging.info("Local padrão: folha-ms/arquivos/")

    # gerar_analise()

    # [TODO] se tiver algum outro tipo para a query, inserir.
    # tipos = ('orgao', 'vinculo', 'cargo', 'situacao')

    menu = '''
                 menu 
    # [1] Inserir dados da folha de pagamentos no banco
    # [2] Efetuar análise por vínculo
    # [3] Efetuar análise por orgão
    # [4] Efetuar análise por cargo
    # [5] Efetuar análise situação
    # [6] Todas as ações acima.
    # [7] Gerar gráficos (svg) das análises.
    # [8] Gerar página estática (html). 
    # [0] Sair. 

    '''

    while True:
        opc = int(input(menu))
        if opc == 0:
            break
        elif opc == 1:
            atualizar_db()
        elif opc == 2:
            gerar_analise('vinculo')
        elif opc == 3:
            gerar_analise('orgao')
        elif opc == 4:
            gerar_analise('cargo')
        elif opc == 5:
            gerar_analise('situacao')
        elif opc == 6:
            atualizar_db()
            for tipo in ('orgao', 'vinculo', 'cargo', 'situacao'):
                gerar_analise(tipo)
        else:
            log.info('Não implementado.')

    logging.info("Concluído!")