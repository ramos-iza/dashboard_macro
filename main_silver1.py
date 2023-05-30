import config 
import pandas as pd 
import silver_data.read_silver_data as rd
import silver_data.transform_silver as ts
import silver_data.save_silver_data as ssd
import datetime
from ast import Assign
import plotly.graph_objects as go 


#Calc IPCA Anual
# Read
ipca_mensal = rd.read_csv(config.silver['ipca_anual']['read_path'])
# Transform
ipca_anual = ts.calc_ipca_anual(ipca_mensal)
# Save
ssd.save_csv(
  df=ipca_anual, 
  path=config.silver['ipca_anual']['save_path']
)

#IPCA Focus
#Read
ipca_anual = rd.read_csv(config.silver['ipca_anual']['save_path'])
ipca_focus = rd.read_csv(config.silver['ipca_focus']['read_path'])
#transform 
dict_focus = ts.criar_dfs_anos_focus(ipca_anual=ipca_anual, ipca_focus=ipca_focus)
#criar_dfs_merge = ts.criar_dfs_merge(dict_focus=dict_focus)

dataframe_2019 = ts.criar_dfs_merge(dict_focus=dict_focus['merge_2019'])
dataframe_2020 = ts.criar_dfs_merge(dict_focus=dict_focus['merge_2020'])
dataframe_2021 = ts.criar_dfs_merge(dict_focus=dict_focus['merge_2021'])
dataframe_2022 = ts.criar_dfs_merge(dict_focus=dict_focus['merge_2022'])
dataframe_2023 = ts.criar_dfs_merge(dict_focus=dict_focus['merge_2023'])
# Save 
ssd.save_csv(
    df=ipca_focus, 
    path=config.silver['ipca_focus']['save_path']    
)
ssd.save_csv(
    df=dataframe_2019, 
    path=config.silver['dataframe_2019']['save_path']
)

ssd.save_csv(
    df=dataframe_2020, 
    path=config.silver['dataframe_2020']['save_path']
)

ssd.save_csv(
    df=dataframe_2021, 
    path=config.silver['dataframe_2021']['save_path']
)

ssd.save_csv(
    df=dataframe_2022, 
    path=config.silver['dataframe_2022']['save_path']
)
ssd.save_csv(
    df=dataframe_2023, 
    path=config.silver['dataframe_2023']['save_path']
)


#Grupos IPCA 
#read
dados_brutos_ipca_sidra = rd.ler_csv(config.raw['dados_brutos_ipca_sidra']['path'])
#Transform
ipca_analise = ts.trat_grupo_ipca(dados_brutos_ipca_sidra=dados_brutos_ipca_sidra)
df_geral_ipca = ts.cal_df_geral_ipca(ipca_analise=ipca_analise)
indice_geral = ts.indice_geral(ipca_analise=ipca_analise)
#save

ssd.save_csv(
    df=ipca_analise,
    path=config.silver['ipca_analise']['save_path']
)

ssd.save_csv(
    df=df_geral_ipca, 
    path=config.silver['df_geral_ipca']['save_path']
)

ssd.save_csv(
    df=indice_geral, 
    path=config.silver['indice_geral']['save_path']
)


#Proporcão
#Transform 
proporcao = ts.calc_proporcao(df_geral_ipca=df_geral_ipca)

'''  
fig = go.Figure(data=[go.Pie(labels=proporcao[0], values=proporcao[1])])
fig.update_layout(title_text='Coparação das variações dos grupos do IPCA - 03/2023')
fig.show()'''
