import pandas as pd


ipca_mensal = {
    'start_date' : '2013-05-04', 
    'path': '/Users/izadoraramos/code/dados/ipca_mensal.csv'
    }
    
    
def ler_csv(caminho):
    ipca_mensal = pd.read_csv(caminho)
    return ipca_mensal
  

def ler_csv(caminho): 
    ipca_focus = pd.read_csv(caminho)
    return ipca_focus


def ler_csv(caminho): 
    dados_brutos_ipca_sidra = pd.read_csv(caminho)
    return dados_brutos_ipca_sidra

def ler_csv(caminho):
    ipca_rm = pd.read_csv(caminho)
    return ipca_rm


def ler_csv(caminho):
    ipca_nucleo = pd.read_csv(caminho)
    return ipca_nucleo

