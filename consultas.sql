# .  Copyright (C) 2020   Jhonathan P. Banczek (jpbanczek@gmail.com)
#

-- DB Browser for SQL
--
-- 100 maiores salarios por remuneração base
-- :data
--
select 
f.nome as NOME,
f.orgao as ORGÃO,
f.situacao as SITUAÇÃO,
F.CARGO AS CARGO,
replace(f.rem_base, '.', ',') as REM_BASE,
replace(f.outras_verbas, '.', ',') as OUTRAS_VERBAS,
replace(f.rem_posdeducoes, '.', ',') as REM_POS_DEDUCOES,
f.vinculo as VÍNCULO,
f.matricula as MATRÍCULA

from folha f where f.competencia like :data
order by f.rem_base desc 
limit 100


--
-- 100 maiores salarios por Remuneração Após Deduções Obrigatórias
--
select 

f.nome as NOME,
f.orgao as ORGÃO,
f.situacao as SITUAÇÃO,
F.CARGO AS CARGO,
replace(f.rem_base, '.', ',') as REM_BASE,
replace(f.outras_verbas, '.', ',') as OUTRAS_VERBAS,
replace(f.rem_posdeducoes, '.', ',') as REM_POS_DEDUCOES,
f.vinculo as VÍNCULO,
f.matricula as MATRÍCULA

from folha f where f.competencia like :data
order by f.rem_posdeducoes desc 
limit 100


--
--  maiores salarios por [orgao/vinculo/situacao/
-- cargo] ordenado do Remuneração Após Deduções Obrigatórias
--
select 

f.nome as NOME,
f.orgao as ORGÃO,
f.situacao as SITUAÇÃO,
F.CARGO AS CARGO,
replace(f.rem_base, '.', ',') as REM_BASE,
replace(f.outras_verbas, '.', ',') as OUTRAS_VERBAS,
replace(f.rem_posdeducoes, '.', ',') as REM_POS_DEDUCOES,
f.vinculo as VÍNCULO,
f.matricula as MATRÍCULA

from folha f where 
f.competencia like :data and 
:filtro like :valor_filtro
order by f.rem_posdeducoes desc 
limit :quantidade

--
-- Somatório - Situação
--
select 
replace(total(f.rem_posdeducoes), '.', ',') as total_REM_POS_DEDUCOES, f.situacao

from folha f where 
f.competencia like '03/2020'
GROUP by f.situacao

--
-- Somatório - ORGAO
--
select 
replace(total(f.rem_posdeducoes), '.', ',') as total_REM_POS_DEDUCOES, f.orgao

from folha f where 
f.competencia like '03/2020'
GROUP by f.orgao

--
-- Somatório - Vinculo
--
select 
replace(total(f.rem_posdeducoes), '.', ',') as total_REM_POS_DEDUCOES, f.vinculo

from folha f where 
f.competencia like '03/2020'
GROUP by f.vinculo

# [TODO]
--
-- CREATE VIEW VINTEMAIORES_032020 AS
-- 
CREATE VIEW VINTEMAIORES_032020 AS
select 
f.nome,
f.orgao,
f.situacao,
F.CARGO,
f.rem_base,
f.outras_verbas,
f.rem_posdeducoes,
f.vinculo,
f.matricula
from folha f where 
f.competencia like '03/2020'
order by f.rem_posdeducoes desc
limit 15280

-- 
-- Somatório
-- VIEW VINTEMAIORES_032020 AS
-- 
select 
replace(total(v.rem_posdeducoes), '.', ',') as total_REM_POS_DEDUCOES 
from VINTEMAIORES_032020 v
