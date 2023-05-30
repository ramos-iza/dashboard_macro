import pandas as pd
import pandas as pd 
import datetime
from ast import Assign
import plotly.graph_objects as go 
#import raw_data.save_raw_data as srd
import pandas as pd 


def calc_ipca_anual(ipca_mensal):
  ipca_mensal['Date'] = pd.to_datetime(ipca_mensal['Date'])
  ipca_mensal['ipca_anual'] = (ipca_mensal['ipca_mensal']/100)+1
  
  ipca_anual = ipca_mensal.groupby(ipca_mensal['Date'].dt.year).prod()['ipca_anual'] -1
  return ipca_anual.to_frame()

def transformar_data_em_datetime(df, nome_coluna, format):
    df[nome_coluna] = pd.to_datetime(df[nome_coluna])

   
#Focus  
def criar_dfs_anos_focus(ipca_anual, ipca_focus):
    ipca_focus = ipca_focus.query('baseCalculo == 0')
    transformar_data_em_datetime(ipca_focus, 'Data', format='%Y-%m-%d')
    ipca_focus = ipca_focus[['Indicador', 'Data', 'DataReferencia', 'Mediana']]

    ipca_ano_2019 = None    
    for h in range(6, 11):
        if h == 6:
            ipca_ano_2019 = pd.DataFrame(ipca_anual.iloc[h]).transpose()
            #ipca_ano_2019 = transformar_data_em_datetime(ipca_ano_2019, 'Date', format='%Y')
        if h == 7:    
            ipca_ano_2020 = pd.DataFrame(ipca_anual.iloc[h]).transpose()
        if h == 8:
            ipca_ano_2021 = pd.DataFrame(ipca_anual.iloc[h]).transpose()
        if h == 9:
            ipca_ano_2022 = pd.DataFrame(ipca_anual.iloc[h]).transpose()
        if h == 10:
            ipca_ano_2023 = pd.DataFrame(ipca_anual.iloc[h]).transpose()
      

    ano = [2019, 2020, 2021, 2022, 2023]
    dataframes_por_ano = {}
    for c in ano:
        dataframes_por_ano[c] = ipca_focus[ipca_focus['DataReferencia'] == c].copy()

    focus_2019 = dataframes_por_ano[2019]
    focus_2020 = dataframes_por_ano[2020]
    focus_2021 = dataframes_por_ano[2021]
    focus_2022 = dataframes_por_ano[2022]
    focus_2023 = dataframes_por_ano[2023]    
    
    lista = [2019, 2020, 2021, 2022, 2023]     
    varios_anos_focus = []        
    focus_anos = [focus_2019, focus_2020, focus_2021, focus_2022, focus_2023]
    for n in focus_anos: 
        for i in range(0, 5):
            if n.equals(focus_anos[i]): 
                varios_anos_focus.append(focus_anos[i])
        df_focus_ano = pd.DataFrame(pd.concat(varios_anos_focus))
    
    df_2019 = df_focus_ano.query('DataReferencia == 2019')
    df_2020 = df_focus_ano.query('DataReferencia == 2020')
    df_2021 = df_focus_ano.query('DataReferencia == 2021')
    df_2022 = df_focus_ano.query('DataReferencia == 2022')
    df_2023 = df_focus_ano.query('DataReferencia == 2023')

    df_2019_ano = df_2019.groupby(df_2019['Data'].dt.strftime('%Y-%m')).mean()['Mediana'].to_frame()
    df_2020_ano = df_2020.groupby(df_2020['Data'].dt.strftime('%Y-%m')).mean()['Mediana'].to_frame()
    df_2021_ano = df_2021.groupby(df_2021['Data'].dt.strftime('%Y-%m')).mean()['Mediana'].to_frame()
    df_2022_ano = df_2022.groupby(df_2022['Data'].dt.strftime('%Y-%m')).mean()['Mediana'].to_frame()
    df_2023_ano = df_2023.groupby(df_2023['Data'].dt.strftime('%Y-%m')).mean()['Mediana'].to_frame()

    merge_2019 = df_2019_ano.join(ipca_ano_2019, how = 'outer')
    merge_2019 = merge_2019.fillna(merge_2019.iloc[-1])
    merge_2019 = merge_2019.iloc[:-1]
    merge_2019['Mediana'] = merge_2019['Mediana']/100

    merge_2020 = df_2020_ano.join(ipca_ano_2020, how = 'outer')
    merge_2020 = merge_2020.fillna(merge_2020.iloc[-1])
    merge_2020 = merge_2020.iloc[:-1]
    merge_2020['Mediana'] = merge_2020['Mediana']/100

    merge_2021 = df_2021_ano.join(ipca_ano_2021, how = 'outer')
    merge_2021 = merge_2021.fillna(merge_2021.iloc[-1])
    merge_2021 = merge_2021.iloc[:-1]
    merge_2021['Mediana'] = merge_2021['Mediana']/100
    
    merge_2022 = df_2022_ano.join(ipca_ano_2022, how = 'outer')
    merge_2022 = merge_2022.fillna(merge_2022.iloc[-1])
    merge_2022 = merge_2022.iloc[:-1]
    merge_2022['Mediana'] = merge_2022['Mediana']/100
    
    merge_2023 = df_2023_ano.join(ipca_ano_2023, how = 'outer')
    merge_2023 = merge_2023.fillna(merge_2023.iloc[-1])
    merge_2023 = merge_2023.iloc[:-1]
    merge_2023['Mediana'] = merge_2023['Mediana']/100
    
    dict_focus = {
        'merge_2019' : merge_2019,
        'merge_2020' : merge_2020, 
        'merge_2021' : merge_2021, 
        'merge_2022' : merge_2022, 
        'merge_2023' : merge_2023
        }
    return dict_focus

def criar_dfs_merge(dict_focus):
    dataframes = dict_focus.iloc[:-1]
    return dataframes


