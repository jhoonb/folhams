# folhams


- [folhams](#folhams)
	- [Modo de usar:](#modo-de-usar)
		- [Teste](#teste)
		- [Gerar/atualizar Banco de Dados:](#geraratualizar-banco-de-dados)
		- [Consultas](#consultas)
	- [Modelo de dados](#modelo-de-dados)
		- [Descrição dos Dados](#descri%c3%a7%c3%a3o-dos-dados)
		- [Tabela Folha](#tabela-folha)
		- [Tabela Item](#tabela-item)
		- [Tabela Analise](#tabela-analise)
	- [dados](#dados)
		- [situação:](#situa%c3%a7%c3%a3o)
		- [orgão:](#org%c3%a3o)
		- [vínculo:](#v%c3%adnculo)
		- [cargo:](#cargo)
		- [[TODO]](#todo)


[em desenvolvimento]

Análise da **Folha de Pagamento** do Estado do Mato Grosso do Sul.  
Dados obtidos no [portal da transparência](http://www.transparencia.ms.gov.br/).  
Dados Abertos: <http://www.dados.ms.gov.br/>  
*Dados a partir de 2018.*

* [Python 3.8.1](https://python.org)
* [Sqlite 3](https://www.sqlite.org/index.html)
* [Pony ORM](https://github.com/ponyorm/pony)


## Modo de usar:

### Teste

Execute o teste:

```
$ python -m unittest -v test.py
```

### Gerar/atualizar Banco de Dados:


```
$ python database.py 
```

ou

```
$ python database.py -main
```

para gerar arquivo .csv com a lista de nomes, cargos, vínculos, situação, orgão:

```
$ python database.py -main -gerar
```


### Consultas

```python

from folhams import FolhaMS

folha = FolhaMS()

query = {
	'competencia': '08/2019',
	'nome': 'JOAO DAMASCENO',
	'cargo': 'PROFESSOR',
	'orgao': 'SED',
	'situacao': 'ATIVO',
	'vinculo': '',
	'matricula': '123456789'
}

# gera a query
folha.select(query)
# executa
folha.execute()
# resultado é um dict
print(folha.res)
print(folha.res['media_rem_apos'])

```

Objeto dict **res**:

```python
res = { 
	'media_rem_base': 0.0, # media da remuneracao base
	'media_outras_verbas': 0.0, # media de outras verbas
	'media_rem_apos': 0.0, # media da remunerção após deduções obrigatórias
	'soma_rem_base': 0.0, # soma da remuneração base
	'soma_outras_verbas': 0.0, # soma outras verbas
	'soma_rem_apos': 0.0 # soma da remuneração após deduções obrigatórias
	}
```

A query pode conter 1 ou mais chaves, todas são concatenadas com o operador **and** na consulta:

```python

from folhams import FolhaMS

folha = FolhaMS()

query = {
	'competencia': '08/2019',
	'orgao': 'SED'
}
# gera a query
folha.select(query)
# executa
folha.execute()

folha.res
```

## Modelo de dados

Essas análises podem ser feitas de maneira agrupada, por:

- Situação
- Orgão
- Vínculo
- Cargo
- Nome
- Competência
  

### Descrição dos Dados

<img src="https://raw.githubusercontent.com/jhoonb/folhams/master/db.png" 
height="238" width="417">


### Tabela Folha


| campo                                    | tipo  | obrigatório |
| ---------------------------------------- | ----- | ----------- |
| arquivo_nome                             | str   | True        |
| quantidade_registros                     | str   | True        |
| link                                     | str   | True        |
| gerado_analise                           | str   | True        |


### Tabela Item

Relação Mensal das informações referentes à remuneração dos servidores públicos – ativos e inativos –, dos empregados públicos e dos pensionistas da Administração Pública Direta e Indireta.


| campo                                    | tipo  | obrigatório |
| ---------------------------------------- | ----- | ----------- |
| competencia                              | str   | True        |
| orgao                                    | str   | True        |
| situacao                                 | str   | True        |
| nome                                     | str   | True        |
| cargo                                    | str   | True        |
| remuneracao_base                         | float | True        |
| outras_verbas                            | float | True        |
| remuneracao\_apos_deducoes\_obrigatorias | float | True        |
| vinculo                                  | str   | True        |
| matricula                                | str   | True        |
| remuneracao_base                         | float | True        |

Observação sobre os campos:

- **Remuneração Base:** (remuneracao_base) Composta pelas parcelas remuneratórias correspondentes ao subsídio, vencimento ou soldo, acrescidas das vantagens pecuniárias pessoais, das vantagens inerentes ao cargo e das vantagens percebidas em caráter permanente.

- **Outras Verbas:** (outras_verbas) Valores pagos em decorrência de acertos de meses anteriores, exercícios anteriores e decisões judiciais, bem como aqueles referentes à gratificação natalina, ao adicional de férias e às verbas indenizatórias.

- **Remuneração Após Deduções Obrigatórias:** (remuneracao\_apos\_deducoes_obrigatorias) Valor da remuneração, descontadas a dedução do teto constitucional e as deduções obrigatórias.


### Tabela Analise

| campo                                 | tipo  | obrigatório |
| ------------------------------------- | ----- | ----------- |
| tipo                                  | str   | True        |
| descricao                             | str   | True        |
| competencia                           | str   | True        |
| media\_remuneracao_base               | float | True        |
| media\_outras_verbas                  | float | True        |
| media\_remuneracao\_apos_deducoes     | float | True        |
| somatorio\_remuneracao_base           | float | True        |
| somatorio\_outras_verbas              | float | True        |
| somatorio\_remuneracao\_apos_deducoes | float | True        |


Observação sobre os campos:
- tipo: 'orgao', 'vinculo', 'cargo', 'situacao'
- descricao: os dados abaixo para cada tipo.


## dados

### situação:

| SITUAÇÃO |
| ---- 
|ATIVO
|INATIVO - APOSENTADO
|INATIVO - PENSÃO POR MORTE


### orgão:

| ORGÃO |
| ----
|AEM-MS
|AGEHAB
|AGEPAN
|AGEPEN
|AGESUL
|AGRAER
|CBMMS
|CGE
|DETRAN
|DGPC
|ESCOLAGOV
|FCMS
|FERTEL
|FUNDECT
|FUNDESPORTE
|FUNDTUR
|FUNSAU
|FUNTRAB
|GOVERNADORIA
|IAGRO
|IMASUL
|JUCEMS
|PGE
|PMMS
|SAD
|SECC
|SED
|SEDHAST
|SEFAZ
|SEGOV
|SEINFRA
|SEJUSP
|SEMAGRO
|SES
|UEMS


### vínculo:

| VÍNCULO
| -----------------
|AGENTE POLITICO
|AGEPREV
|BOLSISTA
|COMISSIONADO REGIME GERAL
|COMISSIONADO REGIME PROPRIO
|CVMRR (CONVOCADO DA RESERVA)
|ESTATUTARIO
|MAGISTÉRIO CONVOCADO
|RESERVA ATIVA
|SERVIDOR REGIME CLT


### cargo: 

| CARGO
| ---------------------------------
|A REGULARIZAR
|ADMINISTRAÇÃO SUPERIOR DIRETA
|ADMINISTRAÇÃO SUPERIOR E ASSESSORAMENTO
|ADVOGADO
|AGENTE CONDUTOR DE VEÍCULOS
|AGENTE DE APOIO INSTITUCIONAL
|AGENTE DE ATIVIDADES CULTURAIS
|AGENTE DE ATIVIDADES DE TRÂNSITO
|AGENTE DE ATIVIDADES EDUCACIONAIS
|AGENTE DE AÇÕES DE TRABALHO
|AGENTE DE AÇÕES SOCIAIS
|AGENTE DE AÇÕES SOCIOEDUCACIONAIS
|AGENTE DE DESENVOLVIMENTO RURAL
|AGENTE DE POLÍCIA CIENTÍFICA
|AGENTE DE POLÍCIA JUDICIÁRIA
|AGENTE DE SEGUR SOCIOEDUCATIVA
|AGENTE DE SEGUR SOCIOEDUCATIVA - MED
|AGENTE DE SEGURANÇA PATRIM. 1ª CATEGORIA
|AGENTE DE SEGURANÇA PATRIM. 2º CATEGORIA
|AGENTE DE SEGURANÇA PATRIM. 3ª CATEGORIA
|AGENTE DE SERVIÇOS AGROPECUÁRIOS
|AGENTE DE SERVIÇOS DE COMUNICAÇÃO
|AGENTE DE SERVIÇOS GRÁFICOS
|AGENTE DE SERVIÇOS OPERACIONAIS
|AGENTE DE SERVIÇOS ORGANIZACIONAIS
|AGENTE DE SERVIÇOS SOCIOORGANIZACIONAIS
|AGENTE FAZENDÁRIO
|AGENTE FISCAL AGROPECUÁRIO
|AGENTE FISCAL DE RELAÇÕES DE CONSUMO
|AGENTE METROLÓGICO
|AGENTE PENITENCIÁRIO ESTADUAL
|ALUNO OFICIAL
|ANALISTA AMBIENTAL
|ANALISTA DE ARTES GRÁFICAS
|ANALISTA DE ATIVIDADES MERCANTIS
|ANALISTA DE MED SOCIOEDUCATIVA
|ANALISTA DE PLANEJAMENTO E ORÇAMENTO
|ANALISTA DE PROG. E PROJ. HABITACIONAIS
|ANALISTA DE PROGRAMAS HABITACIONAIS
|ANALISTA DE RECURSOS HÍDRICOS
|ANALISTA DE REGULAÇÃO
|ANALISTA DE TECNOLOGIA DA INFORMAÇÃO
|ANALISTA DESENVOLVIMENTO SOCIOECONÔMICO
|ANALISTA FAZENDÁRIO
|ASSESSOR
|ASSESSOR DE PROCURADOR
|ASSESSOR ESPECIAL
|ASSESSOR II
|ASSESSOR JURÍDICO
|ASSESSOR TÉCNICO
|ASSESSORAMENTO SUPERIOR
|ASSISTENTE
|ASSISTENTE DE ATIVIDADES CULTURAIS
|ASSISTENTE DE ATIVIDADES DE TRÂNSITO
|ASSISTENTE DE ATIVIDADES EDUCACIONAIS
|ASSISTENTE DE ATIVIDADES MERCANTIS
|ASSISTENTE DE AÇÕES DE TRABALHO
|ASSISTENTE DE AÇÕES SOCIAIS
|ASSISTENTE DE CAPTAÇÃO DE VAGAS
|ASSISTENTE DE DESENVOLV. SOCIOECONÔMICO
|ASSISTENTE DE RELAÇÕES DE CONSUMO
|ASSISTENTE DE SERVIÇOS DE COMUNICAÇÃO
|ASSISTENTE DE SERVIÇOS DE SAÚDE I
|ASSISTENTE DE SERVIÇOS DE SAÚDE II
|ASSISTENTE DE SERVIÇOS OPERACIONAIS
|ASSISTENTE DE SERVIÇOS ORGANIZACIONAIS
|ASSISTENTE I
|ASSISTENTE II
|ASSISTENTE III
|ASSISTENTE TÉCNICO DE NÍVEL MÉDIO
|ASSISTENTE TÉCNICO DE ORÇAMENTO
|AUDITOR DE SERVIÇOS DE SAÚDE
|AUDITOR DO ESTADO
|AUDITOR EST. DE CONTR EXTERNO
|AUDITOR FISCAL DA REC ESTADUAL
|AUXILIAR DE ATIVIDADES EDUCACIONAIS
|AUXILIAR DE SERVIÇOS AGROPECUÁRIOS
|AUXILIAR DE SERVIÇOS BÁSICOS
|AUXILIAR DE SERVIÇOS ESPECIALIZADOS
|AUXILIAR DE SERVIÇOS GRÁFICOS
|AUXILIAR DE SERVIÇOS OPERACIONAIS
|AUXILIAR DE SERVIÇOS ORGANIZACIONAIS
|AUXILIAR FAZENDÁRIO
|AUXILIAR METROLÓGICO
|Assistente Técnico Operacional
|BOLSA ATLETA
|BOLSA ESTUDOS FUNDECT
|CABOS E SOLDADOS
|CHEFE DE ASSESSORIA
|CHEFE DE DEPARTAMENTO
|CHEFE DE DIVISÃO
|CHEFE DE GABINETE
|CHEFE DE PROCURADORIA
|CHEFE DE UNIDADE
|CHEFE DE UNIDADE REGIONAL
|CONTRATO PUBLICO
|CONTROLADOR-GERAL
|CONTROLADOR-GERAL ADJUNTO
|COORDENADOR
|COORDENADOR DE UNIDADE
|COORDENADOR ESPECIAL
|COORDENADOR GERAL
|COORDENADOR REGIONAL
|COORDENADORIA
|CORPO VOLUNT.DE MIL.INATIVOS
|CORREGEDOR-GERAL DA AGEPEN-MS
|CURSO DE FORMAÇÃO
|DAP
|DELEGADO DE POLICIA
|DIRETOR
|DIRETOR ADJUNTO
|DIRETOR DE DIRETORIA
|DIRETOR GERAL
|DIRETOR PRESIDENTE
|DIRETOR-EXECUTIVO
|DIREÇÃO ESPECIAL E ASSESSORAMENTO
|DIREÇÃO EXECUTIVA E ASSESSORAMENTO
|DIREÇÃO EXECUTIVA SUPERIOR E ASSESSORAME
|DIREÇÃO GERENCIAL E ASSESSORAMENTO
|DIREÇÃO GERENCIAL SUPERIOR E ASSESSORAME
|DIREÇÃO INTERMEDIÁRIA E ASSESSORAMENTO
|DIREÇÃO SUPERIOR E ASSESSORAMENTO
|DIREÇÃO SUPERIOR ESPECIAL E ASSESSORAMEN
|EM EXTINÇÃO
|ESPECIALISTA DE EDUCAÇÃO - 30H
|ESPECIALISTA DE EDUCAÇÃO - 36H
|ESPECIALISTA DE SERVIÇOS DE SAÚDE
|EX-GOVERNADOR
|FISCAL AMBIENTAL
|FISCAL DE OBRAS HABITACIONAIS
|FISCAL DE OBRAS PÚBLICAS
|FISCAL DE RELAÇÕES DE CONSUMO
|FISCAL DE VIGILÂNCIA SANITÁRIA
|FISCAL ESTADUAL AGROPECUÁRIO
|FISCAL TRIBUTÁRIO ESTADUAL
|FUNÇÃO DE CONFIANÇA
|GERENTE
|GERENTE DE AGENCIA REGIONAL I
|GERENTE DE AGENCIA REGIONAL II
|GERENTE DE AGÊNCIA III
|GERENTE DE PROGRAMA
|GERENTE GERAL
|GERENTE REGIONAL
|GERÊNCIA EXECUTIVA E ASSESSORAMENTO
|GESTOR AMBIENTAL
|GESTOR DE APOIO OPERACIONAL
|GESTOR DE ATIV. DE DESENV.SOCIOECONÔMICO
|GESTOR DE ATIVIDADES AGROPECUÁRIAS
|GESTOR DE ATIVIDADES CULTURAIS
|GESTOR DE ATIVIDADES DE TRÂNSITO
|GESTOR DE ATIVIDADES DESPORTIVAS
|GESTOR DE ATIVIDADES EDUCACIONAIS
|GESTOR DE AÇÕES DE TRABALHO
|GESTOR DE AÇÕES SOCIAIS
|GESTOR DE AÇÕES SOCIOEDUCACIONAIS
|GESTOR DE CIÊNCIA E TECNOLOGIA
|GESTOR DE DESENVOLVIMENTO RURAL
|GESTOR DE PROCESSO
|GESTOR DE PROCESSO II
|GESTOR DE RELAÇÕES DE CONSUMO
|GESTOR DE SERVIÇOS ORGANIZACIONAIS
|GESTOR ESTADUAL AGROPECUÁRIO
|GESTOR REGIONAL
|GESTOR SOCIOORGANIZACIONAL RURAL
|GESTÃO E ASSISTÊNCIA
|GESTÃO INTERMEDIÁRIA E ASSISTÊNCIA
|GESTÃO OPERACIONAL E ASSISTÊNCIA
|GOVERNADOR
|GUARDA PARQUE
|INSPETOR DE AÇÕES SOCIOEDUCACIONAIS
|OFICIAIS INTERMEDIÁRIOS
|OFICIAIS SUBALTERNOS
|OFICIAIS SUPERIORES
|OUTROS PODERES
|OUVIDOR
|PERITO OFICIAL FORENSE
|PERITO PAPILOSCOPISTA
|PESQUISADOR
|PRAÇAS EM SITUAÇÃO ESPECIAL
|PRAÇAS ESPECIAIS
|PROCURADOR DE ENTIDADES PÚB. - ESPECIAL
|PROCURADOR DE ENTIDADES PÚBLICAS- 1ª CAT
|PROCURADOR DE ENTIDADES PÚBLICAS- 2ª CAT
|PROCURADOR DE ENTIDADES PÚBLICAS- 3ª CAT
|PROCURADOR DO ESTADO - 1ª CATEGORIA
|PROCURADOR DO ESTADO - 2ª CATEGORIA
|PROCURADOR DO ESTADO - 3ª CATEGORIA
|PROCURADOR DO ESTADO - CATEGORIA INICIAL
|PROCURADOR DO ESTADO -CATEGORIA ESPECIAL
|PROFESSOR
|PROFESSOR CONVOCADO
|PROFESSOR DE ENSINO SUPERIOR
|PROFESSOR LEIGO
|PROFISSIONAL ATIVIDADES DE COMUNICAÇÃO
|PROFISSIONAL DE NÍVEL SUPERIOR
|PROFISSIONAL DE SERVIÇOS HOSPITALARES
|PRÓ-REITOR
|REITOR
|SECRETÁRIO ADJUNTO
|SECRETÁRIO DE ESTADO
|SECRETÁRIO DE GABINETE
|SECRETÁRIO ESPECIAL
|SECRETÁRIO GERAL
|SUBSECRETÁRIO
|SUBTENENTE E SARGENTOS
|SUPERINTENDENTE
|TECNÓLOGO DE OBRAS PÚBLICAS
|TEMPORÁRIO
|TÉC ADMIN. APOIO GESTÃO REC. HIDRICOS
|TÉCNICO AMBIENTAL
|TÉCNICO DE ARTES GRÁFICAS
|TÉCNICO DE ATIVIDADES CULTURAIS
|TÉCNICO DE ATIVIDADES DE COMUNICAÇÃO
|TÉCNICO DE ATIVIDADES DESPORTIVAS
|TÉCNICO DE CONTROLE EXTERNO
|TÉCNICO DE DESENVOLVIMENTO RURAL
|TÉCNICO DE NÍVEL SUPERIOR
|TÉCNICO DE PROGRAMAS HABITACIONAIS
|TÉCNICO DE REGULAÇÃO
|TÉCNICO DE SERVIÇOS AMBIENTAIS
|TÉCNICO DE SERVIÇOS DE ENGENHARIA
|TÉCNICO DE SERVIÇOS HOSPITALARES I
|TÉCNICO DE SERVIÇOS HOSPITALARES II
|TÉCNICO DE SERVIÇOS OPERACIONAIS
|TÉCNICO DE SERVIÇOS ORGANIZACIONAIS
|TÉCNICO DE TECNOLOGIA DA INFORMAÇÃO
|TÉCNICO EM AUDITORIA
|TÉCNICO FAZENDÁRIO
|TÉCNICO METROLÓGICO
|TÉCNICO PENITENCIÁRIO
|TÉNICO DE APOIO INSTITUCIONAL
|VICE-DIRETOR PRESIDENTE
|VICE-GOVERNADOR
|VICE-REITOR


### [TODO] 

Para a melhor visualização da análise será implementada a geração de gráficos usando a biblioteca [*pygal.*](https://github.com/Kozea/pygal/tree/master/pygal/graph)