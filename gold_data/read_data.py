import pandas as pd 

def ler_csv(caminho): 
    ipca_anual = pd.read_cvs(caminho)
    return ipca_anual
   