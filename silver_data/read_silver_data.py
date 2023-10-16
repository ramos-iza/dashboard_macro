import pandas as pd


ipca_mensal = {
    'start_date' : '2013-05-04', 
    'path': '/Users/izadoraramos/code/dados/ipca_mensal.csv'
    }
    
    
def read_csv(path):
    df = pd.read_csv(path)
    return df
  

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

def ler_csv(caminho):
    pib_volume_trimestral = pd.read_csv(caminho)
    return pib_volume_trimestral

def ler_csv(caminho):
    db_trimestre_sazional = pd.read_csv(caminho)
    return db_trimestre_sazional

def ler_csv(caminho):
    db_taxa_desemprego = pd.read_csv(caminho)
    return db_taxa_desemprego


def ler_csv(caminho):
    db_taxa_desemprego = pd.read_csv(caminho)
    return db_taxa_desemprego

def ler_csv(caminho):
    db_tipos_emprego = pd.read_csv(caminho)
    return db_tipos_emprego


def ler_csv(caminho):
    db_desempre_sexo = pd.read_csv(caminho)
    return db_desempre_sexo


def ler_csv(caminho):
    dados_credito = pd.read_csv(caminho)
    return dados_credito


def ler_csv(caminho):
    ipca_credito = pd.read_csv(caminho)
    return ipca_credito