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

