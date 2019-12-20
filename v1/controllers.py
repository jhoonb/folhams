from typing import NewType, List
import models


@models.db_session
def insert_folha(folha_data: models.FolhaData) -> None:
    """
    insert_folha insere todos os dicts 
    (no formato feito por tratar_arquivo())
    na tabela do banco 'Folha'
    retorno: quantidade de inserts (int)
    """

    for folha_linha in folha_data.linhas:
        models.Folha(
            competencia_mes=folha_linha.competencia_mes,
            competencia_ano=folha_linha.competencia_ano,
            orgao=folha_linha.orgao,
            situacao=folha_linha.situacao,
            nome=folha_linha.nome,
            cpf=folha_linha.cpf,
            cargo=folha_linha.cargo,
            remuneracao_base=folha_linha.base,
            outras_verbas=folha_linha.outras,
            remuneracao_apos_deducoes_obrigatorias=folha_linha.apos,
            vinculo=folha_linha.vinculo,
            matricula=folha_linha.matricula,
            complementar=folha_linha.complementar,
            decimo_terceiro=folha_linha.decimo_terceiro
        )


@models.db_session
def insert_arquivo(nome: str, quantidade: int) -> None:
    models.Arquivo(arquivo_nome=nome, quantidade_registros=quantidade)


@models.db_session
def select_arquivo() -> List[str]:
    """
    select_arquivo retorna uma lista contendo
    todos os valores do campo arquivo_nome da tabela Arquivo
    retorno: list
    """
    arquivos = list(models.select(c.arquivo_nome for c in models.Arquivo))
    return arquivos


# analise de dados
@models.db_session
def analise(tipo: str, ano: str, mes: str, complementar: bool,
            decimo_terceiro: bool) -> None:

    # verifica se já não foi inserido
    v_inserido = list(
        models.select(c.codigo for c in models.Controle
                      if c.tipo == tipo
                      and c.competencia_ano == ano
                      and c.competencia_mes == mes
                      and c.complementar == complementar
                      and c.decimo_terceiro == decimo_terceiro))

    # se foi inserido pula...
    # se for folha de 13º, valida apenas se for mês 12,
    # do contrário não faz query
    if v_inserido or (decimo_terceiro and mes != '12'):
        return None

    # todos os tipos 
    # ['orgao', 'vinculo', 'cargo', 'situacao'] - distinct
    tipos = None
    if tipo == 'orgao':
        tipos = list(
            models.select(f.orgao for f in models.Folha
                          if f.competencia_ano == ano
                          and f.competencia_mes == mes
                          and f.complementar == complementar
                          and f.decimo_terceiro == decimo_terceiro))
    elif tipo == 'vinculo':
        tipos = list(
            models.select(f.vinculo for f in models.Folha
                          if f.competencia_ano == ano
                          and f.competencia_mes == mes
                          and f.complementar == complementar
                          and f.decimo_terceiro == decimo_terceiro))
    elif tipo == 'cargo':
        tipos = list(
            models.select(f.cargo for f in models.Folha
                          if f.competencia_ano == ano
                          and f.competencia_mes == mes
                          and f.complementar == complementar
                          and f.decimo_terceiro == decimo_terceiro))
    elif tipo == 'situacao':
        tipos = list(
            models.select(f.situacao for f in models.Folha
                          if f.competencia_ano == ano
                          and f.competencia_mes == mes
                          and f.complementar == complementar
                          and f.decimo_terceiro == decimo_terceiro))
    else:
        print(f"Tipo {tipo} NÃO IMPLEMENTADO")

    # nao retornou resultado [None] na busca
    if not tipos:
        return None

    for t in tipos:
        print(f"Consultando e inserindo dados: {t}")

        d = {}
        d['tipo'] = tipo
        d['descricao'] = t

        # analise = Analise()
        # analise.tipo = tipo
        # analise.descricao = t


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

            d['media_pos'] = models.avg((f.remuneracao_apos_deducoes_obrigatorias
                                         for f in models.Folha
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

            d['soma_pos'] = models.sum((f.remuneracao_apos_deducoes_obrigatorias
                                        for f in models.Folha
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

            d['media_pos'] = models.avg((f.remuneracao_apos_deducoes_obrigatorias
                                         for f in models.Folha
                                         if f.vinculo == t
                                         and f.competencia_ano == ano
                                         and f.competencia_mes == mes
                                         and f.complementar == complementar
                                         and f.decimo_terceiro == decimo_terceiro), distinct=False)

            d['soma_rem_base'] = models.sum((f.remuneracao_base
                                             for f in models.Folha
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

            d['soma_pos'] = models.sum((f.remuneracao_apos_deducoes_obrigatorias
                                        for f in models.Folha
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

            d['media_pos'] = models.avg((f.remuneracao_apos_deducoes_obrigatorias
                                         for f in models.Folha
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

            d['soma_pos'] = models.sum((f.remuneracao_apos_deducoes_obrigatorias
                                        for f in models.Folha
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

            d['media_pos'] = models.avg((f.remuneracao_apos_deducoes_obrigatorias
                                         for f in models.Folha
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

            d['soma_pos'] = models.sum((f.remuneracao_apos_deducoes_obrigatorias
                                        for f in models.Folha
                                        if f.situacao == t
                                        and f.competencia_ano == ano
                                        and f.competencia_mes == mes
                                        and f.complementar == complementar
                                        and f.decimo_terceiro == decimo_terceiro), distinct=False)

        else:
            print(f"Tipo {tipo} NÃO IMPLEMENTADO")

        # testar se não retornou nada
        # insere no banco tabela Analise
        if d['soma_outras'] and d['soma_pos'] and d['soma_rem_base']:
            models.Analise(tipo=d['tipo'],
                           descricao=d['descricao'],
                           competencia_ano=ano,
                           competencia_mes=mes,
                           media_remuneracao_base=d['media_rem_base'],
                           media_outras_verbas=d['media_outras'],
                           media_remuneracao_apos_deducoes=d['media_pos'],
                           somatorio_remuneracao_base=d['soma_rem_base'],
                           somatorio_outras_verbas=d['soma_outras'],
                           somatorio_remuneracao_apos_deducoes=d['soma_pos'],
                           complementar=complementar,
                           decimo_terceiro=decimo_terceiro)
        else:
            print("Query SQL Não retornou resultados ")

    # inserir controle
    models.Controle(tipo=tipo,
                    competencia_ano=ano,
                    competencia_mes=mes,
                    complementar=complementar,
                    decimo_terceiro=decimo_terceiro)
