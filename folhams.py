import os
import logging
import itertools
from pathlib import Path
import sqlite3
import models

_caminho_arquivo = os.getcwd() + "/arquivos/"
logging.basicConfig(level=logging.INFO)

# 
def buscar_arquivos():
    # apenas o nome do arquivo
    f_nome = lambda s: str(s).split("/")[-1]
    p = Path(_caminho_arquivo)
    arquivos = [f_nome(i) for i in p.iterdir() if i.is_file()]
    return arquivos


def ler_arquivo(arquivo_nome):
    with open(_caminho_arquivo + arquivo_nome, 'r') as f:
        d = f.readlines()
    return d


def ler_arquivos(arquivos_local):
    d = []
    for arquivo_nome in arquivos_local:
        d.append(ler_arquivo(arquivo_nome))
    return d


@models.db_session
def tratar_arquivo(arquivo):

    def f_formata_float(d):
        d = d.replace('"', '')
        d = d.replace(',', '.')
        return float(d)

    folha = {}

    f_complementar = lambda x: True if 'COMP' in x else False
    f_decimo_terceiro = lambda x: True if '13' in x else False 

    # ignora cabeçalho [1:]
    for linha in arquivo[1:]:
        s = linha.split(";")
        mes, ano = s[0].split("/")
        folha['competencia-mes'] = mes
        folha['competencia-ano'] = ano[:4]
        folha['orgao'] = s[1]
        folha['situacao'] = s[2]
        folha['nome'] = s[3]
        folha['cpf'] = s[4]
        folha['cargo'] = s[5]
        folha['base'] = f_formata_float(s[6])
        folha['outras'] = f_formata_float(s[7])
        folha['apos'] = f_formata_float(s[8])
        folha['vinculo'] = s[9]
        folha['matricula'] = s[10]
        folha['complementar'] = f_complementar(ano[4:])
        folha['decimo_terceiro'] = f_decimo_terceiro(ano[4:])

        # insert na tabela
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
    return len(arquivo[1:])

    
@models.db_session
def inserir_tab_arquivo_folha(dados, arquivos_local):
    logging.info('Folhas de pagamentos para analisar e inserir: {}'.format(len(dados))) 
    for i, arquivo in enumerate(dados):
        logging.info("Analisando e inserindo {} registros... Aguarde".format(len(arquivo[1:]))) 
        tam = tratar_arquivo(arquivo)
        # insert na tabela folha / arquivo
        models.Arquivo(arquivo_nome=arquivos_local[i], quantidade_registros=tam)
        logging.info("Inserida a folha: {}".format(arquivos_local[i]))


@models.db_session
def atualizar_db():
    dados_bd = list(models.select(c.arquivo_nome for c in models.Arquivo))
    arquivos_local = buscar_arquivos()
    arquivos_local = [i for i in arquivos_local if i not in dados_bd]
    dados = ler_arquivos(arquivos_local)
    inserir_tab_arquivo_folha(dados, arquivos_local)


## analise de dados
@models.db_session
def analiseOrgao(ano, mes, complementar, decimo_terceiro):

    # verifica se jã não foi inserido
    v = list(models.select(c.codigo for c in models.Controle if c.tabela == 'AnaliseOrgao' 
        and c.competencia_ano == ano 
        and c.competencia_mes == mes 
        and c.complementar == complementar
        and c.decimo_terceiro == decimo_terceiro))

    # se foi inserido pula...
    logging.info("Consulta tabela: Controle {}".format(v))
    if v:
        return 


    # todos os orgãos - distinct
    orgaos = list(models.select(f.orgao for f in models.Folha if f.competencia_ano == ano 
        and f.competencia_mes == mes and f.complementar == complementar
        and f.decimo_terceiro == decimo_terceiro))
    
    # nao retornou resultado [None] na busca
    if not orgaos:
        logging.info("Orgão: nao retornou resultado na busca")
        return

    for orgao in orgaos:
        logging.info("Consultando e inserindo dados do orgão: {}".format(orgao))

        d = {'orgao': orgao,

        'qnt_registros': models.count((f for f in models.Folha if f.competencia_ano == ano 
            and f.competencia_mes == mes and f.orgao == orgao and 
            f.complementar == complementar and 
            f.decimo_terceiro == decimo_terceiro), distinct=False),

        'media_rem_base': models.avg((f.remuneracao_base for f in models.Folha if f.competencia_ano == ano 
            and f.competencia_mes == mes and 
            f.orgao == orgao and f.complementar == complementar and 
            f.decimo_terceiro == decimo_terceiro), distinct=False),

        'media_outras': models.avg((f.outras_verbas for f in models.Folha if f.competencia_ano == ano 
            and f.competencia_mes == mes and f.orgao == orgao and 
            f.complementar == complementar and 
            f.decimo_terceiro == decimo_terceiro), distinct=False),

        'media_pos': models.avg((f.remuneracao_apos_deducoes_obrigatorias for f in models.Folha if f.competencia_ano == ano 
            and f.competencia_mes == mes and 
            f.orgao == orgao and f.complementar == complementar and 
            f.decimo_terceiro == decimo_terceiro), distinct=False),

        'soma_rem_base': models.sum((f.remuneracao_base for f in models.Folha if f.competencia_ano == ano 
            and f.competencia_mes == mes and f.orgao == orgao and 
            f.complementar == complementar and 
            f.decimo_terceiro == decimo_terceiro), distinct=False),

        'soma_outras': models.sum((f.outras_verbas for f in models.Folha if f.competencia_ano == ano 
            and f.competencia_mes == mes and 
            f.orgao == orgao and f.complementar == complementar and 
            f.decimo_terceiro == decimo_terceiro), distinct=False),

        'soma_pos': models.sum((f.remuneracao_apos_deducoes_obrigatorias for f in models.Folha if f.competencia_ano == ano 
            and f.competencia_mes == mes and f.orgao == orgao and 
            f.complementar == complementar and 
            f.decimo_terceiro == decimo_terceiro), distinct=False)  
        }

        # testar se não retornou nada
        # insere no banco tabela AnaliseOrgao
        if d['soma_outras'] and d['soma_pos'] and d['soma_rem_base']:
            models.AnaliseOrgao(orgao = d['orgao'], 
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
    models.Controle(tabela="AnaliseOrgao",
        competencia_ano = ano,
        competencia_mes = mes,
        complementar = complementar,
        decimo_terceiro = decimo_terceiro)


def gerar_analiseOrgao():

    meses = ('01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12')
    anos = ('2018', '2019')
    # gera com as combinacoes de folha com decimo terceiro e/ou complementar
    for decimo_terceiro, complementar in itertools.product((True, False), repeat=2):
        logging.info("Decimo terceiro: {} | complementar: {}".format(decimo_terceiro, complementar))
        for ano in anos:
            for mes in meses:
                logging.info("ANO: {} | MES: {}".format(ano, mes))
                analiseOrgao(ano, mes, complementar, decimo_terceiro)


#######################################################################
if __name__ == '__main__':

    logging.info("Analise da folha de pagamento do Estado do Mato Grosso do Sul")    
    logging.info("Buscando arquivos da folha de pagamento do Estado no armazenamento local...")
    logging.info("Local padrão: folha-ms/arquivos/")

    atualizar_db()
    gerar_analiseOrgao()
    logging.info("Concluído!")