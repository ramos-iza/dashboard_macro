import pandas as pd 
from bcb import sgs 
import sidrapy as sidra
from bcb import Expectativas 
import ipeadatapy as ipea
from statsmodels.tsa import x13
import os


def ipca_mensal(start_date): 
    ipca_mensal = sgs.get(codes= '433', start= start_date).rename(columns= {'433' : 'ipca_mensal'})
    return ipca_mensal


'''def dados_brutos_ipca_sidra():
    variable= ['63', '69', '2265', '66']
    dados_brutos_ipca = pd.DataFrame()
    for var in variable:
        df = sidra.get_table(
            table_code= '7060', 
            territorial_level= '1', 
            ibge_territorial_code= 'all', 
            period= 'all',
            variable= var, 
            classification= '315/all')
        dados_brutos_ipca = pd.concat([df, dados_brutos_ipca], axis=0)
    return dados_brutos_ipca'''
    

def dados_brutos_ipca_sidra():
    variables = ['63', '69', '2265', '66']
    dados_brutos_ipca = pd.DataFrame()

    # Define periods explicitly in YYYYMM format
    periods = [
        '202101', '202102', '202103', '202104', '202105', '202106', '202107', '202108', '202109', '202110',
        '202111', '202112', '202201', '202202', '202203', '202204', '202205', '202206', '202207', '202208',
        '202209', '202210', '202211', '202212', '202301', '202302', '202303', '202304', '202305', '202306',
        '202307', '202308', '202309', '202310', '202311', '202312', '202401', '202402', '202403', '202404',
        '202405', '202406', '202407', '202408', '202409', '202410', '202411', '202412', '202501', '202502',
        '202503', '202504'
    ]

    for var in variables:
        for period in periods:
            try:
                df = sidra.get_table(
                    table_code='7060', 
                    territorial_level='1', 
                    ibge_territorial_code='all', 
                    period=period,
                    variable=var, 
                    classification='315/all'
                )
                dados_brutos_ipca = pd.concat([dados_brutos_ipca, df], axis=0)
            except ValueError as e:
                print(f"Error fetching data for variable {var} and period {period}: {e}")
                continue
    
    return dados_brutos_ipca


def ipca_focus():
    em = Expectativas()
    exp_ipca = em.get_endpoint('ExpectativasMercadoAnuais')
    ipca_focus = (exp_ipca.query().filter(exp_ipca.Indicador == 'IPCA').filter(exp_ipca.Data >= '2013-05-04').collect())
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
                    #period = "all",
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


def db_credito():
    # Parâmetros e códigos para coleta de dados
    codigos = {
    # Concessões de crédito - Total - R$ (milhões)
    "Concessões de crédito - Total": 20631,

    # Concessões de crédito - Pessoas jurídicas - Total - R$ (milhões)
    "Concessões de crédito - PJ": 20632,

    # Concessões de crédito - Pessoas físicas - Total	- R$ (milhões)
    "Concessões de crédito - PF": 20633,

    # Concessões de crédito com recursos livres - Total	- R$ (milhões)
    "Concessões de crédito - Livre": 20634,

    # Concessões de crédito com recursos direcionados - Total	- R$ (milhões)
    "Concessões de crédito - Direcionado": 20685,

    # Saldo da carteira de crédito - Total - R$ (milhões)
    "Saldo da carteira de crédito - Total": 20539,

    # PIB acumulado dos últimos 12 meses - Valores correntes - (R$ milhões)
    "PIB acumulado dos últimos 12 meses": 4382,

    # Saldos das operações de crédito sob controle privado - Total	- (R$ milhões)
    "Saldos de crédito - Privado": 2043,

    # Saldos das operações de crédito sob controle público - Total	- (R$ milhões)
    "Saldos de crédito - Público": 2007,

    # Taxa média de juros das operações de crédito - Total - % a.a.
    "Taxa média de juros das operações de crédito": 20714,

    # Spread médio das operações de crédito - Total	- p.p.
    "Spread médio das operações de crédito": 20783,

    # Inadimplência da carteira de crédito - Total - %
    "Inadimplência da carteira de crédito": 21082

    }

    # Importa dados do SGS/BCB
    dados = sgs.get(codes = codigos, start = "2012-01-01")
    return dados
    
    
def ipca_cred():
    # Importa dados do IPCA
    ipca = sidra.get_table(
        table_code = "1737", 
        territorial_level = "1", 
        ibge_territorial_code = "all", 
        variable = "2266", 
        period = "all"
        )
    return ipca


def sgs_m1():
    m1 = sgs.get(codes= '27785').rename(columns= { '27785': 'm1'})
    return m1

def dados_brutos_ipca_15():
    variable= ['355', '1120']
    dados_brutos_ipca_15 = pd.DataFrame()
    for var in variable:
        df = sidra.get_table(
            table_code= '3065', 
            territorial_level= '1', 
            ibge_territorial_code= 'all', 
            period= 'last 120',
            variable= var)
        dados_brutos_ipca_15 = pd.concat([df, dados_brutos_ipca_15], axis=0)
    return dados_brutos_ipca_15



