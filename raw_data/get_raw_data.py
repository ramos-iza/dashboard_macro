import pandas as pd 
from bcb import sgs 
import sidrapy as sidra
from bcb import Expectativas 
import ipeadatapy as ipea


def ipca_mensal(start_date): 
    ipca_mensal = sgs.get(codes= '433', start= start_date).rename(columns= {'433' : 'ipca_mensal'})
    return ipca_mensal


def dados_brutos_ipca_sidra():
    variable= ['63', '69', '2265', '66']
    dados_brutos_ipca = pd.DataFrame()
    for var in variable:
        df = sidra.get_table(
            table_code= '7060', 
            territorial_level= '1', 
            ibge_territorial_code= 'all', 
            period= 'last 120',
            variable= var, 
            classification= '315/all')
        dados_brutos_ipca = pd.concat([df, dados_brutos_ipca], axis=0)
    return dados_brutos_ipca


def ipca_focus():
    em = Expectativas()
    em.describe()
    exp_ipca = Expectativas().get_endpoint('ExpectativasMercadoAnuais')
    ipca_focus = (exp_ipca.query().filter(exp_ipca.Indicador == 'IPCA').filter(exp_ipca.Data >= '2013-05-04').collect())
    ipca_focus.info()
    return ipca_focus


def ipca_rm(): 
    variable= ['69']
    ipca_rm = pd.DataFrame()
    for var in variable:
        df = sidra.get_table(
            table_code= '7060', 
            territorial_level= '7', 
            ibge_territorial_code= 'all', 
            period= 'last 120',
            variable= var, 
            classification= '315/7169')
        ipca_rm = pd.concat([df, ipca_rm], axis=0)
    return ipca_rm


def ipca_nucleo(): 
    ipca_nucleo = sgs.get(codes = {
    'IPCA-EX0' : 11427,
    'IPCA-EX1' : 16121,
    'IPCA-EX2' : 27838,
    'IPCA-EX3' : 27839,
    'IPCA-MA' : 4466,
    'IPCA-MS' : 11426,
    'IPCA-DP' : 16122,
    'IPCA-P55' : 28750	
    }
    , start = '2000-01-01')
    return ipca_nucleo

# PIB 
def pib_volume_trimestral():
    pib_volume_trimestral = sidra.get_table(
                table_code = 1620,
                territorial_level = "1",
                ibge_territorial_code = "all",
                variable = 583,
                classifications = {
                    "11255": "90687,90691,90696,90707,93404,93405,93406,93407,93408"
                    },
                period = "all"
                )
    return pib_volume_trimestral

def db_trimestre_sazional():
    db_trimestre_sazional = sidra.get_table(
                table_code = 1621,
                territorial_level = "1",
                ibge_territorial_code = "all",
                variable = 584,
                classifications = {
                    "11255": "90687,90691,90696,90707,93404,93405,93406,93407,93408"
                    },
                period = "all"
                )
    return db_trimestre_sazional
    
def db_taxa_desemprego():
    db_taxa_desemprego = sidra.get_table(table_code = 6381,
                    territorial_level = "1",
                    ibge_territorial_code = "all",
                    period = "all"
                    )
    return db_taxa_desemprego


def db_tipos_emprego():
    db_tipos_emprego = sidra.get_table(table_code = 6320,
                    territorial_level = "1",
                    ibge_territorial_code = "all",
                    period = "all",
                    classification= '11913/all'
                    )
    return db_tipos_emprego


def db_grandes_regioes():
    db_grandes_regioes = sidra.get_table(table_code = '4099',
                    territorial_level = "2",
                    ibge_territorial_code = "all",
                    variable = '4099',
                    period = "all")
    return db_grandes_regioes\
        
 
def db_desempre_sexo():       
    db_desempre_sexo = sidra.get_table(table_code = '4093',
                    territorial_level = "1",
                    ibge_territorial_code = "all",
                    variable = '4099',
                    period = "all",
                    classifications= {
                        "2": "6794,4,5"
                        })
    return db_desempre_sexo


def db_pop_idade():
    db_pop_idade = sidra.get_table(table_code = '4094',
                    territorial_level = "1",
                    ibge_territorial_code = "all",
                    variable = '4099',
                    period = "all",
                    classifications= {
                        "58": "95253,114535,100052,108875,99127,3302"
                        })
    return db_pop_idade


def rendimento_regiao():
    rendimento_regiao = sidra.get_table(table_code = '5437',
                    territorial_level = '2',
                    ibge_territorial_code = "all",
                    variable = '5932',
                    period = "all",
                    classifications= {
                        "58": "95253,114535,100052,108875,99127,3302"
                        })
    return rendimento_regiao


def rendimento_regiao_br():
    rendimento_regiao_br = sidra.get_table(table_code = '5437',
                territorial_level = '1',
                ibge_territorial_code = "all",
                variable = '5932',
                period = "all",
                classifications= {
                    "58": "95253,114535,100052,108875,99127,3302"
                    })
    return rendimento_regiao_br 

# Caged 
import ipeadatapy as ipea
# Ver metadados
metadados_ipea = ipea.metadata()
metadados_ipea

# Identificar código do CAGED nos metadados 
metadados_ipea[metadados_ipea.NAME.str.contains('Caged')]

# Coletar dados 
def dados_admissoes():
    dados_admissoes = ipea.timeseries('CAGED12_ADMISN12')
    return dados_admissoes 

def dados_demissoes():
    dados_demissoes = ipea.timeseries('CAGED12_DESLIGN12')
    return dados_demissoes

def dados_saldo():
    dados_saldo = ipea.timeseries('CAGED12_SALDON12')
    return dados_saldo




