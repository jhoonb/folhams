import sys
import models
import json
import folhams


__datas__ = ('01/2018', '02/2018', '03/2018', '04/2018', '05/2018', '06/2018',
             '07/2018', '08/2018', '09/2018', '10/2018', '11/2018', '12/2018',
             '01/2019', '02/2019', '03/2019', '04/2019', '05/2019', '06/2019',
             '07/2019', '08/2019', '09/2019', '10/2019', '11/2019', '12/2019')

__limite__ = 5


@models.orm.db_session
def salarios_entre() -> None:

    valores = {}

    valores = ((0, 5_000), (5_001, 10_000), (10_001, 15_000), (15_001, 20_000),
               (20_001, 25_000), (25_001, 30_000), (30_001, 35_000),
               (35_001, 40_000), (40_001, 45_000), (45_001, 50_000),
               (50_001, 55_000), (55_001, 60_000), (60_001, 65_000), 
               (65_001, 70_000), (70_001, 75_000), (75_001, 80_000), 
               (80_001, 85_000), (85_001, 90_000), 
               (90_001, 95_000), (95_001, 100_000), 
               (100_001, 1_000_000_000))

    sql = """
    select *
    from item i where i.competencia like '{0}' 
    and i.remuneracao_apos_deducoes_obrigatorias between
    {1} and {2} """

    res = {}

    for data in __datas__:

        res[data] = {}

        for valor in valores:

            query = sql.format(data, valor[0], valor[1])
            print("query: ", query)

            dado = models.Item.select_by_sql(query)
            qnt = len(dado)
            soma = sum(
                [i.remuneracao_apos_deducoes_obrigatorias for i in dado])
            d = {
                'quantidade': qnt,
                'soma': soma,
                'media': soma / (qnt if qnt != 0 else 1)
            }

            chave_valor = f'{valor[0]}-{valor[1]}'
            res[data][chave_valor] = d

    folhams.tojson(res, 'salarios_entre.json')


@models.orm.db_session
def situacao_por_mes() -> None:
    res = {}
    for data in __datas__:
        query = models.orm.select((i.situacao, models.orm.count())
                                  for i in models.Item
                                  if i.competencia == data)
        res[data] = {}
        for situacao, quantidade in query:
            res[data][situacao] = quantidade

    folhams.tojson(res, 'situacao_por_mes.json')


@models.orm.db_session
def maior_salario_por_cargo() -> None:
    res = {}
    cargos = folhams.select_tipo("cargo")

    print('qnt de cargos: ', len(cargos))

    for data in __datas__:
        res[data] = {}
        print(f"----------------{data}--------------")
        for cargo in cargos:
            #res[data][cargo] = []
            print(f'-> {cargo}')
            query = models.orm.select(
                i for i in models.Item
                if i.competencia == data and i.cargo == cargo)

            a = lambda y: y.remuneracao_apos_deducoes_obrigatorias
            query = sorted(query, key=a)
            query.reverse()
            # os 20 maiores
            res[data][cargo] = [(
                i.nome, i.orgao, i.vinculo, i.matricula, 
                i.situacao,
                i.remuneracao_apos_deducoes_obrigatorias) 
                for i in query[:__limite__]]

    folhams.tojson(res, 'maior_salario_cargo.json')


@models.orm.db_session
def maior_salario_por_orgao() -> None:
    res = {}
    orgaos = folhams.select_tipo("orgao")

    print('qnt de orgaos: ', len(orgaos))

    for data in __datas__:
        res[data] = {}
        print(f"----------------{data}--------------")
        for orgao in orgaos:
            #res[data][orgao] = []
            print(f'-> {orgao}')
            query = models.orm.select(
                i for i in models.Item
                if i.competencia == data and i.orgao == orgao)

            a = lambda y: y.remuneracao_apos_deducoes_obrigatorias
            query = sorted(query, key=a)
            query.reverse()
            # os 20 maiores
            res[data][orgao] = [(
                i.nome, i.cargo, i.vinculo,
                i.matricula, i.situacao, 
                i.remuneracao_apos_deducoes_obrigatorias) 
                for i in query[:__limite__]]

    folhams.tojson(res, 'maior_salario_orgao.json')


@models.orm.db_session
def maior_salario_por_vinculo() -> None:
    res = {}
    vinculos = folhams.select_tipo("vinculo")

    print('qnt de vinculos: ', len(vinculos))

    for data in __datas__:
        res[data] = {}
        print(f"----------------{data}--------------")
        for vinculo in vinculos:
            #res[data][vinculo] = []
            print(f'-> {vinculo}')
            query = models.orm.select(
                i for i in models.Item
                if i.competencia == data and i.vinculo == vinculo)

            a = lambda y: y.remuneracao_apos_deducoes_obrigatorias
            query = sorted(query, key=a)
            query.reverse()
            # os 20 maiores
            res[data][vinculo] = [(
                i.nome, i.cargo, i.orgao,
                i.matricula, i.situacao, 
                i.remuneracao_apos_deducoes_obrigatorias) 
                for i in query[:__limite__]]

    folhams.tojson(res, 'maior_salario_vinculo.json')


@models.orm.db_session
def maior_salario_por_situacao() -> None:
    res = {}
    situacoes = folhams.select_tipo("situacao")

    print('qnt de situacoes: ', len(situacoes))

    for data in __datas__:
        res[data] = {}
        print(f"----------------{data}--------------")
        for situacao in situacoes:
            #res[data][situacao] = []
            print(f'-> {situacao}')
            query = models.orm.select(
                i for i in models.Item
                if i.competencia == data and i.situacao == situacao)

            a = lambda y: y.remuneracao_apos_deducoes_obrigatorias
            query = sorted(query, key=a)
            query.reverse()
            # os 20 maiores
            res[data][situacao] = [(
                i.nome, i.cargo, i.orgao,
                i.vinculo, i.matricula,
                i.remuneracao_apos_deducoes_obrigatorias) 
                for i in query[:__limite__]]

    folhams.tojson(res, 'maior_salario_situacao.json')


@models.orm.db_session
def maiores_salario() -> None:

    res = {}
    for data in __datas__:
        print(f"----------------{data}--------------")
        query = models.orm.select(
            i for i in models.Item
            if i.competencia == data)

        a = lambda y: y.remuneracao_apos_deducoes_obrigatorias
        query = sorted(query, key=a)
        query.reverse()
        # os 200 maiores
        res[data] = [(
            i.nome, i.cargo, i.orgao,
            i.vinculo, i.situacao, i.matricula,
            i.remuneracao_apos_deducoes_obrigatorias) 
            for i in query[:200]]

    folhams.tojson(res, 'maiores_salario.json')


def html_gen():
    html_select = """
    <select> 
    {}
    </select> 
    """

    html = """<!DOCTYPE html>
    <html>
    <head>
        <meta charset='utf-8'>
        <title>FolhaMS</title>
        <meta name='viewport' content='width=device-width, initial-scale=1'>
        <!--<link rel='stylesheet' type='text/css' media='screen' href='main.css'> -->
    </head>
    <body>
        {}
    </body>
    </html>
    """

    tag = '<option value="{0}">{0}</option>\n'
    with open("maiores_salario.json", "r") as f:
        data = json.load(f)

    tags = ""
    for k, v in data.items():
        tags += tag.format(k)

    fa = html.format(html_select.format(tags))
    with open('index.html', 'w') as f:
        f.write(fa)
    


if __name__ == "__main__":

    tipo = sys.argv[1]
    print(tipo)
    if tipo == 'cargo':
        maior_salario_por_cargo()
    elif tipo == 'orgao':
        maior_salario_por_orgao()
    elif tipo == 'situacao':
        maior_salario_por_situacao()
    elif tipo == 'vinculo':
        maior_salario_por_vinculo()
    elif tipo == 'mes':
        situacao_por_mes()
    elif tipo == 'salario':
        maiores_salario()
    elif tipo == 'html':
        html_gen()
    else:
        print("param tipo")
        print("""
        consulta.py [cargo, situacao, orgao, vinculo, mes, salario]
        """)