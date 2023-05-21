def soma(numero1, numero2):
    return numero1+numero2

import pandas as pd 
from bcb import sgs 
import sidrapy as sidra

def ipca_mensal(start_date): 
    ipca_mensal = sgs.get(codes= '433', start= start_date).rename(columns= {'433' : 'ipca_mensal'})
    return ipca_mensal




