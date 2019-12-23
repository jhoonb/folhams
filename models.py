from pony import orm

db = orm.Database("sqlite", "database.sqlite3", create_db=True)


class Folha(db.Entity):
    arquivo_nome = orm.Required(str)
    quantidade_registros = orm.Required(int)
    link = orm.Required(str)
    gerado_analise = orm.Required(bool)
    itens = orm.Set('Item')
    analise_folhas = orm.Set('AnaliseFolha')


class Item(db.Entity):
    folha = orm.Required(Folha)
    competencia = orm.Required(str)
    orgao = orm.Required(str)
    situacao = orm.Required(str)
    nome = orm.Required(str)
    cargo = orm.Required(str)
    remuneracao_base = orm.Required(float)
    outras_verbas = orm.Required(float)
    remuneracao_apos_deducoes_obrigatorias = orm.Required(float)
    vinculo = orm.Required(str)
    matricula = orm.Required(str)


class AnaliseFolha(db.Entity):
    folha = orm.Required(Folha)
    tipo = orm.Required(str)
    descricao = orm.Required(str)
    competencia = orm.Required(str)
    soma_rem_base = orm.Required(float)
    soma_outras_verbas = orm.Required(float)
    soma_rem_apos_deducoes = orm.Required(float)    
    media_rem_base = orm.Required(float)
    media_outras_verbas = orm.Required(float)
    media_rem_apos_deducoes = orm.Required(float)


class Tipo(db.Entity):
    tipo = orm.Required(str)
    descricao = orm.Required(str)


db.generate_mapping(create_tables=True)
