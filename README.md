# folhams

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

A query pode conter 1 ou mais chaves, todas são concatenas como o operador **and** na consulta:

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



[TODO] ...
E efetuará cálculos de média e somatório
para os valores da folha: 

- remuneracao_base (somatório e média)
- outras_verbas (somatório e média)
- remuneracao\_apos_deducoes\_obrigatorias (somatório e média)


Essas análises podem ser feitas de maneira agrupada, por:

- Situação
- Orgão
- Vínculo
- Cargo
- Nome
- Competência

### [TODO] 

Para a melhor visualização da análise será implementada a geração de gráficos usando a biblioteca [*pygal.*](https://github.com/Kozea/pygal/tree/master/pygal/graph)


## Descrição dos Dados

- [folhams](#folhams)
	- [Modo de usar:](#modo-de-usar)
		- [Teste](#teste)
		- [Gerar/atualizar Banco de Dados:](#geraratualizar-banco-de-dados)
		- [Consultas](#consultas)
	- [Modelo de dados](#modelo-de-dados)
		- [[TODO]](#todo)
	- [Descrição dos Dados](#descri%c3%a7%c3%a3o-dos-dados)
		- [Tabela Folha](#tabela-folha)
		- [Tabela Analise](#tabela-analise)
	- [Análise](#an%c3%a1lise)
		- [por situação:](#por-situa%c3%a7%c3%a3o)
		- [por orgão:](#por-org%c3%a3o)
		- [por vínculo:](#por-v%c3%adnculo)
		- [por cargo:](#por-cargo)


### Tabela Folha

Relação Mensal das informações referentes à remuneração dos servidores públicos – ativos e inativos –, dos empregados públicos e dos pensionistas da Administração Pública Direta e Indireta.


| campo                                    | tipo  | obrigatório |
| ---------------------------------------- | ----- | ----------- |
| competencia_ano                          | str   | True        |
| competencia_mes                          | str   | True        |
| orgao                                    | str   | True        |
| situacao                                 | str   | True        |
| nome                                     | str   | True        |
| cpf                                      | str   | True        |
| cargo                                    | str   | True        |
| remuneracao_base                         | float | True        |
| outras_verbas                            | float | True        |
| remuneracao\_apos_deducoes\_obrigatorias | float | True        |
| vinculo                                  | str   | True        |
| matricula                                | str   | True        |
| complementar                             | bool  | True        |
| decimo_terceiro                          | bool  | True        |
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
| competencia_ano                       | str   | True        |
| competencia_mes                       | str   | True        |
| media\_remuneracao_base               | float | True        |
| media\_outras_verbas                  | float | True        |
| media\_remuneracao\_apos_deducoes     | float | True        |
| somatorio\_remuneracao_base           | float | True        |
| somatorio\_outras_verbas              | float | True        |
| somatorio\_remuneracao\_apos_deducoes | float | True        |
| complementar                          | bool  | True        |
| decimo_terceiro                       | bool  | True        |


Observação sobre os campos:
- tipo: 'orgao', 'vinculo', 'cargo', 'situacao'
- descricao: os dados abaixo para cada tipo.


## Análise 

### por situação:

| SITUAÇÃO |
| ---- 
| INATIVO - APOSENTADO
| ATIVO
| INATIVO - PENSÃO POR MORTE


### por orgão:

| ORGÃO |
| ----
| orgao
|AGEPREV
|SED
|SEDHAST
|CBMMS
|AGRAER
|DGPC
|SEGOV
|AGESUL
|PMMS
|AGEPEN
|DETRAN
|SEJUSP
|PGE
|AGEHAB
|IAGRO
|FUNSAU
|SAD
|UEMS
|AEM-MS
|FUNTRAB
|FUNDECT
|FERTEL
|SEFAZ
|SES
|FUNDESPORTE
|IMASUL
|JUCEMS
|FUNDTUR
|FCMS
|CGE
|SEMAGRO
|SEINFRA
|AGEPAN
|SECC
|GOVERNADORIA
|ESCOLAGOV


### por vínculo:

| VÍNCULO
| -----------------
|ESTATUTARIO
|MAGISTÉRIO CONVOCADO
|COMISSIONADO REGIME GERAL
|AGENTE POLITICO
|COMISSIONADO REGIME PROPRIO
|BOLSISTA
|AGEPREV
|RESERVA ATIVA
|CONTRATO PUBLICO
|CVMRR (CONVOCADO DA RESERVA)
|SERVIDOR REGIME CLT


### por cargo: 

| CARGO
| ---------------------------------
|AUXILIAR DE ATIVIDADES EDUCACIONAIS
|PROFESSOR
|A REGULARIZAR
|TÉCNICO FAZENDÁRIO
|ASSISTENTE DE ATIVIDADES EDUCACIONAIS
|AGENTE DE ATIVIDADES EDUCACIONAIS
|PROFESSOR CONVOCADO
|AGENTE DE AÇÕES DE TRABALHO
|ASSISTENTE DE AÇÕES SOCIAIS
|AGENTE DE SERVIÇOS ORGANIZACIONAIS
|AGENTE PENITENCIÁRIO ESTADUAL
|SUBTENENTE E SARGENTOS
|TÉCNICO DE SERVIÇOS OPERACIONAIS
|CABOS E SOLDADOS
|FISCAL ESTADUAL AGROPECUÁRIO
|AUDITOR FISCAL DA REC ESTADUAL
|AGENTE DE SERVIÇOS SOCIOORGANIZACIONAIS
|FISCAL TRIBUTÁRIO ESTADUAL
|DELEGADO DE POLICIA
|AGENTE DE POLÍCIA JUDICIÁRIA
|ASSISTENTE
|ESPECIALISTA DE EDUCAÇÃO - 36H
|ASSISTENTE DE AÇÕES DE TRABALHO
|AUXILIAR FAZENDÁRIO
|SECRETÁRIO DE ESTADO
|GERENTE DE AGÊNCIA III
|ASSISTENTE DE SERVIÇOS OPERACIONAIS
|ASSISTENTE DE ATIVIDADES DE TRÂNSITO
|AGENTE DE SEGUR SOCIOEDUCATIVA
|TÉCNICO DE PROGRAMAS HABITACIONAIS
|TÉCNICO DE SERVIÇOS HOSPITALARES II
|ASSISTENTE DE SERVIÇOS ORGANIZACIONAIS
|EM EXTINÇÃO
|AGENTE DE SEGURANÇA PATRIM. 2º CATEGORIA
|PROFESSOR DE ENSINO SUPERIOR
|TÉCNICO METROLÓGICO
|ASSISTENTE DE SERVIÇOS DE SAÚDE II
|OFICIAIS SUPERIORES
|DIRETOR
|GESTOR DE ATIVIDADES EDUCACIONAIS
|AGENTE DE AÇÕES SOCIAIS
|BOLSA ESTUDOS FUNDECT
|AGENTE DE SEGURANÇA PATRIM. 3ª CATEGORIA
|OUTROS PODERES
|ASSISTENTE DE SERVIÇOS DE SAÚDE I
|AUXILIAR DE SERVIÇOS ORGANIZACIONAIS
|OFICIAIS SUBALTERNOS
|COORDENADOR
|PROFISSIONAL DE SERVIÇOS HOSPITALARES
|PERITO OFICIAL FORENSE
|PRAÇAS ESPECIAIS
|PROCURADOR DO ESTADO -CATEGORIA ESPECIAL
|ESPECIALISTA DE SERVIÇOS DE SAÚDE
|TÉCNICO DE SERVIÇOS ORGANIZACIONAIS
|GESTOR DE PROCESSO
|FISCAL DE VIGILÂNCIA SANITÁRIA
|DAP
|ASSESSOR II
|PERITO PAPILOSCOPISTA
|AGENTE DE SERVIÇOS AGROPECUÁRIOS
|GESTOR DE ATIVIDADES DE TRÂNSITO
|CONTRATO PUBLICO
|AGENTE DE SERVIÇOS OPERACIONAIS
|TÉCNICO DE ATIVIDADES DE COMUNICAÇÃO
|AGENTE DE SEGURANÇA PATRIM. 1ª CATEGORIA
|BOLSA ATLETA
|AUXILIAR DE SERVIÇOS OPERACIONAIS
|ASSESSOR
|AGENTE FISCAL AGROPECUÁRIO
|FISCAL DE OBRAS PÚBLICAS
|GUARDA PARQUE
|OFICIAIS INTERMEDIÁRIOS
|TÉCNICO DE SERVIÇOS HOSPITALARES I
|TÉCNICO DE ATIVIDADES CULTURAIS
|ANALISTA DE ATIVIDADES MERCANTIS
|CHEFE DE DIVISÃO
|ANALISTA DESENVOLVIMENTO SOCIOECONÔMICO
|PROFESSOR LEIGO
|CORPO VOLUNT.DE MIL.INATIVOS
|ASSESSOR JURÍDICO
|AGENTE DE ATIVIDADES CULTURAIS
|ANALISTA FAZENDÁRIO
|TÉCNICO DE SERVIÇOS DE ENGENHARIA
|AUXILIAR DE SERVIÇOS AGROPECUÁRIOS
|GESTOR DE DESENVOLVIMENTO RURAL
|AGENTE DE POLÍCIA CIENTÍFICA
|SUPERINTENDENTE
|FISCAL DE OBRAS HABITACIONAIS
|AGENTE DE ATIVIDADES DE TRÂNSITO
|ANALISTA DE PROGRAMAS HABITACIONAIS
|GESTOR DE SERVIÇOS ORGANIZACIONAIS
|AGENTE CONDUTOR DE VEÍCULOS
|GESTOR ESTADUAL AGROPECUÁRIO
|ANALISTA DE PLANEJAMENTO E ORÇAMENTO
|AUDITOR DO ESTADO
|AGENTE DE SERVIÇOS GRÁFICOS
|TÉCNICO DE NÍVEL SUPERIOR
|ASSISTENTE II
|GERENTE DE AGENCIA REGIONAL II
|ASSISTENTE TÉCNICO DE NÍVEL MÉDIO
|TÉCNICO EM AUDITORIA
|FISCAL AMBIENTAL
|TÉCNICO AMBIENTAL
|PRÓ-REITOR
|COORDENADOR DE UNIDADE
|PROCURADOR DE ENTIDADES PÚB. - ESPECIAL
|ANALISTA DE MED SOCIOEDUCATIVA
|GESTOR DE ATIVIDADES CULTURAIS
|TÉCNICO DE DESENVOLVIMENTO RURAL
|PROCURADOR DO ESTADO - 2ª CATEGORIA
|SECRETÁRIO ADJUNTO
|ANALISTA AMBIENTAL
|ADVOGADO
|ANALISTA DE TECNOLOGIA DA INFORMAÇÃO
|PROFISSIONAL ATIVIDADES DE COMUNICAÇÃO
|CHEFE DE UNIDADE REGIONAL
|DIRETOR DE DIRETORIA
|ASSISTENTE I
|AGENTE FAZENDÁRIO
|GERENTE
|ASSESSOR TÉCNICO
|PROCURADOR DE ENTIDADES PÚBLICAS- 2ª CAT
|PRAÇAS EM SITUAÇÃO ESPECIAL
|AUXILIAR METROLÓGICO
|GESTOR DE ATIV. DE DESENV.SOCIOECONÔMICO
|ASSISTENTE III
|AUDITOR EST. DE CONTR EXTERNO
|ASSISTENTE DE DESENVOLV. SOCIOECONÔMICO
|ASSESSOR ESPECIAL
|AGENTE METROLÓGICO
|TÉCNICO DE TECNOLOGIA DA INFORMAÇÃO
|GESTOR SOCIOORGANIZACIONAL RURAL
|ASSISTENTE DE SERVIÇOS DE COMUNICAÇÃO
|AUDITOR DE SERVIÇOS DE SAÚDE
|PESQUISADOR
|ANALISTA DE REGULAÇÃO
|PROCURADOR DO ESTADO - 1ª CATEGORIA
|GESTOR DE AÇÕES SOCIAIS
|GERENTE DE AGENCIA REGIONAL I
|FISCAL DE RELAÇÕES DE CONSUMO
|ASSISTENTE DE ATIVIDADES CULTURAIS
|GERENTE GERAL
|GESTOR DE AÇÕES DE TRABALHO
|CHEFE DE UNIDADE
|GESTOR DE RELAÇÕES DE CONSUMO
|CORREGEDOR-GERAL DA AGEPEN-MS
|ASSESSOR DE PROCURADOR
|DIRETOR PRESIDENTE
|DIRETOR GERAL
|TÉCNICO DE REGULAÇÃO
|PROCURADOR DE ENTIDADES PÚBLICAS- 1ª CAT
|GESTOR DE APOIO OPERACIONAL
|COORDENADOR ESPECIAL
|TÉCNICO DE ARTES GRÁFICAS
|ASSISTENTE DE ATIVIDADES MERCANTIS
|COORDENADOR GERAL
|DIRETOR-EXECUTIVO
|ESPECIALISTA DE EDUCAÇÃO - 30H
|PROCURADOR DO ESTADO - 3ª CATEGORIA
|CONTROLADOR-GERAL
|COORDENADORIA
|COORDENADOR REGIONAL
|ANALISTA DE ARTES GRÁFICAS
|TÉCNICO DE ATIVIDADES DESPORTIVAS
|AGENTE FISCAL DE RELAÇÕES DE CONSUMO
|ASSISTENTE DE CAPTAÇÃO DE VAGAS
|GESTOR DE PROCESSO II
|TÉCNICO PENITENCIÁRIO
|AUXILIAR DE SERVIÇOS ESPECIALIZADOS
|AGENTE DE SERVIÇOS DE COMUNICAÇÃO
|AUXILIAR DE SERVIÇOS GRÁFICOS
|GESTOR DE CIÊNCIA E TECNOLOGIA
|TÉNICO DE APOIO INSTITUCIONAL
|OUVIDOR
|ASSISTENTE DE RELAÇÕES DE CONSUMO
|ASSISTENTE TÉCNICO DE ORÇAMENTO
|AUXILIAR DE SERVIÇOS BÁSICOS
|GERENTE REGIONAL
|TÉCNICO DE SERVIÇOS AMBIENTAIS
|SECRETÁRIO ESPECIAL
|CHEFE DE PROCURADORIA
|TECNÓLOGO DE OBRAS PÚBLICAS
|AGENTE DE DESENVOLVIMENTO RURAL
|GESTOR REGIONAL
|SECRETÁRIO DE GABINETE
|AGENTE DE AÇÕES SOCIOEDUCACIONAIS
|REITOR
|EX-GOVERNADOR
|AGENTE DE APOIO INSTITUCIONAL
|GERENTE DE PROGRAMA
|SECRETÁRIO GERAL
|PROCURADOR DE ENTIDADES PÚBLICAS- 3ª CAT
|DIRETOR ADJUNTO
|INSPETOR DE AÇÕES SOCIOEDUCACIONAIS
|CHEFE DE DEPARTAMENTO
|GESTOR DE ATIVIDADES DESPORTIVAS
|GESTOR AMBIENTAL
|PROCURADOR DO ESTADO - CATEGORIA INICIAL
|FUNÇÃO DE CONFIANÇA
|VICE-REITOR
|TÉCNICO DE CONTROLE EXTERNO
|GESTOR DE AÇÕES SOCIOEDUCACIONAIS
|CHEFE DE ASSESSORIA
|CONTROLADOR-GERAL ADJUNTO
|VICE-DIRETOR PRESIDENTE
|CHEFE DE GABINETE
|GOVERNADOR
|PROFISSIONAL DE NÍVEL SUPERIOR
|ANALISTA DE PROG. E PROJ. HABITACIONAIS
|VICE-GOVERNADOR
|GESTOR DE ATIVIDADES AGROPECUÁRIAS
|TEMPORÁRIO
|ALUNO OFICIAL
|SUBSECRETÁRIO
|GESTÃO INTERMEDIÁRIA E ASSISTÊNCIA
|ADMINISTRAÇÃO SUPERIOR DIRETA
|AGENTE DE SEGUR SOCIOEDUCATIVA - MED
|DIREÇÃO GERENCIAL E ASSESSORAMENTO
|DIREÇÃO EXECUTIVA E ASSESSORAMENTO
|GESTÃO E ASSISTÊNCIA
|GERÊNCIA EXECUTIVA E ASSESSORAMENTO
|DIREÇÃO ESPECIAL E ASSESSORAMENTO
|DIREÇÃO INTERMEDIÁRIA E ASSESSORAMENTO
|DIREÇÃO SUPERIOR E ASSESSORAMENTO
|DIREÇÃO SUPERIOR ESPECIAL E ASSESSORAMEN
|DIREÇÃO EXECUTIVA SUPERIOR E ASSESSORAME
|GESTÃO OPERACIONAL E ASSISTÊNCIA
|DIREÇÃO GERENCIAL SUPERIOR E ASSESSORAME
|ASSESSORAMENTO SUPERIOR
|ADMINISTRAÇÃO SUPERIOR E ASSESSORAMENTO
|ANALISTA DE RECURSOS HÍDRICOS
|TÉC ADMIN. APOIO GESTÃO REC. HIDRICOS
|CURSO DE FORMAÇÃO