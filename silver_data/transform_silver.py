import pandas as pd

def calc_ipca_anual(ipca_mensal):
  ipca_mensal['Date'] = pd.to_datetime(ipca_mensal['Date'])
  ipca_mensal['ipca_anual'] = (ipca_mensal['ipca_mensal']/100)+1
  
  ipca_anual = ipca_mensal.groupby(ipca_mensal['Date'].dt.year).prod()['ipca_anual'] -1
  return ipca_anual.to_frame()