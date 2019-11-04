# em desenvolvimento ...

import models

@models.db_session
def gerar_grafico():

    import locale

    query = models.select((a.descricao, 
        a.competencia_ano, 
        a.competencia_mes,
        a.somatorio_remuneracao_apos_deducoes) for a in models.Analise if a.descricao == 'SED')

    query = list(query)

    print(query)

    ano_2018 = [
    sum([q[3] for q in query if q[1] == '2018' and q[2] == '01']),
    sum([q[3] for q in query if q[1] == '2018' and q[2] == '01']),
    sum([q[3] for q in query if q[1] == '2018' and q[2] == '02']),
    sum([q[3] for q in query if q[1] == '2018' and q[2] == '03']),
    sum([q[3] for q in query if q[1] == '2018' and q[2] == '04']),
    sum([q[3] for q in query if q[1] == '2018' and q[2] == '05']),
    sum([q[3] for q in query if q[1] == '2018' and q[2] == '06']),
    sum([q[3] for q in query if q[1] == '2018' and q[2] == '07']),
    sum([q[3] for q in query if q[1] == '2018' and q[2] == '08']),
    sum([q[3] for q in query if q[1] == '2018' and q[2] == '09'])]

    ano_2019 = [
    sum([q[3] for q in query if q[1] == '2019' and q[2] == '01']),
    sum([q[3] for q in query if q[1] == '2019' and q[2] == '01']),
    sum([q[3] for q in query if q[1] == '2019' and q[2] == '02']),
    sum([q[3] for q in query if q[1] == '2019' and q[2] == '03']),
    sum([q[3] for q in query if q[1] == '2019' and q[2] == '04']),
    sum([q[3] for q in query if q[1] == '2019' and q[2] == '05']),
    sum([q[3] for q in query if q[1] == '2019' and q[2] == '06']),
    sum([q[3] for q in query if q[1] == '2019' and q[2] == '07']),
    sum([q[3] for q in query if q[1] == '2019' and q[2] == '08']),
    sum([q[3] for q in query if q[1] == '2019' and q[2] == '09'])]

    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

    f_ = lambda v: locale.currency(v, grouping=True, symbol=None)

    for i, j in zip(ano_2018, ano_2019):
        print("ano 2018 R$: {} | ano 2019 R$: {}".format(f_(i), f_(j)))

        barra = pygal.Bar()
        line_chart.title = 'Comparação da remuneração '