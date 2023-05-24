import config 
import pandas as pd 
import silver_data.read_data as rd
import datetime
from ast import Assign
import plotly.graph_objects as go 


# Mensal
ipca_mensal = rd.ler_csv(config.ipca_mensal['path'])
ipca_mensal_copia = ipca_mensal
ipca_mensal_copia['Date'] = pd.to_datetime(ipca_mensal_copia['Date'])
ipca_mensal_copia['ipca_anual'] = (ipca_mensal_copia['ipca_mensal']/100)+1
ipca_mensal_copia = ipca_mensal_copia.groupby(ipca_mensal_copia['Date'].dt.year).prod()['ipca_anual'] -1
ipca_anual = ipca_mensal_copia.to_frame()

#Focus

def transformar_data_em_datetime(df, nome_coluna, format):
    df[nome_coluna] = pd.to_datetime(df[nome_coluna])

ipca_focus = rd.ler_csv(config.ipca_focus['path'])

ipca_focus = ipca_focus.query('baseCalculo == 0')
transformar_data_em_datetime(ipca_focus, 'Data', format='%Y-%m-%d')
#transformar_data_em_datetime(ipca_focus, 'DataReferencia', format='%Y')
#ipca_focus['DataReferencia'] = ipca_focus['DataReferencia'].dt.year
ipca_focus = ipca_focus[['Indicador', 'Data', 'DataReferencia', 'Mediana']]

for h in range(6, 11):
    df_ano = ipca_anual.iloc[h].to_frame()
    if h == 6:
        ipca_ano_2019 = ipca_anual.iloc[h].to_frame()
    if h == 7:    
        ipca_ano_2020 = ipca_anual.iloc[h].to_frame()
    if h == 8:
        ipca_ano_2021 = ipca_anual.iloc[h].to_frame()
    if h == 9:
        ipca_ano_2022 = ipca_anual.iloc[h].to_frame()
    if h == 10:
        ipca_ano_2023 = ipca_anual.iloc[h].to_frame()
                


#ipca_ano_2019 = ipca_anual.iloc[6].to_frame()

ano = [2019, 2020, 2021, 2022, 2023]
dataframes_por_ano = {}
for c in ano:
    dataframes_por_ano[c] = ipca_focus[ipca_focus['DataReferencia'] == c].copy()

focus_2019 = dataframes_por_ano[2019]
focus_2020 = dataframes_por_ano[2020]
focus_2021 = dataframes_por_ano[2021]
focus_2022 = dataframes_por_ano[2022]
focus_2023 = dataframes_por_ano[2023]
merge_2019 = None 
      
   
lista = [2019, 2020, 2021, 2022, 2023]     
varios_anos_focus = []        
focus_anos = [focus_2019, focus_2020, focus_2022, focus_2022, focus_2023]
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
merge_2019 = merge_2019.fillna(merge_2019.iloc[-1], inplace= True)
#merge_2019 = merge_2019.iloc[:-1]
#merge_2019['Mediana'] = merge_2019['Mediana']/100



'''
fig = go.Figure()
fig.add_trace(go.Scatter(x= df_2019_ano.index, y= merge_2019[2019], name='IPCA 2019'))
fig.add_trace(go.Scatter(x= df_2019_ano.index, y= merge_2019['Mediana'], name='Previsão IPCA p/2019'))
fig.show()'''
