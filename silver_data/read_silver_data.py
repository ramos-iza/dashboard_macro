import pandas as pd


ipca_mensal = {
    'start_date' : '2013-05-04', 
    'path': '/Users/izadoraramos/code/dados/ipca_mensal.csv'
    }
    
    
def read_csv(path):
    df = pd.read_csv(path)
    return df


def ler_csv(caminho):
    df = pd.read_csv(caminho)
    return df