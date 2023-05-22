def soma(numero1, numero2):
    return numero1+numero2

import pandas as pd 
from bcb import sgs 
import sidrapy as sidra
from bcb import Expectativas 


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






