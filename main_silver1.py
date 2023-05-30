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


fig = go.Figure()
fig.add_trace(go.Scatter(name= 'ipca 2020', x = dataframe_2021.index, y = dataframe_2021['ipca_anual']))
fig.add_trace(go.Scatter(name= 'exp ipca 2020', x = dataframe_2021.index, y = dataframe_2021['Mediana']))
fig.show()




