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

#Gráfico é no gold 
fig = go.Figure()
fig.add_trace(go.Scatter(x = merge_2023.index, y = merge_2023['Mediana'], name = 'exp IPCA 2023'))
fig.add_trace(go.Scatter(x = merge_2023.index, y = merge_2023[2023], name = 'IPCA 2023 até agora'))
fig.show()

#Silver gurpos do IPCA

dados_brutos_ipca_sidra = rd.ler_csv(config.dados_brutos_ipca_sidra['path'])

ipca_analise = (dados_brutos_ipca_sidra.rename(columns= dados_brutos_ipca_sidra.iloc[0]).query('Valor not in "Valor"').rename(columns = {
    'Mês (Código)' : 'data', 
    'Valor' : 'valor',
    'Variável' : 'variavel',
    'Geral, grupo, subgrupo, item e subitem' : 'grupo'}).query('valor not in ["valor", "..."]').filter(items= [
        'data', 'variavel', 'grupo', 'valor'], axis='columns').replace(to_replace = {
            'variavel' : {
            'IPCA - Peso mensal' : 'Variação % mensal',
            'IPCA - Variação acumulada em 12 meses' : 'IPCA % acum. 12 meses', 
            'IPCA - Variação acumulada no ano' : 'IPCA % acum. ano', 
            'IPCA - Variação mensal' : 'IPCA peso mensal'
            }
            }, 
            regex = True).assign(data = lambda x: pd.to_datetime(x.data, format = '%Y%m'),
                                 valor = lambda x: x.valor.astype(float)))

ipca_analise = ipca_analise.query('variavel == "IPCA peso mensal"')            

todas_listas = []
for numero in range(1, 10):
  if numero == 1:
    numero_str = str(numero) + '.'
    linhas_com_1 = ipca_analise.loc[ipca_analise['grupo'].str.startswith(numero_str)]
    lista = linhas_com_1.values.tolist()
    todas_listas.append(lista)
    alimentacao_bebidas = pd.concat([pd.DataFrame(lista) for lista in todas_listas], ignore_index=True).rename(columns = {0: 'data', 1:'variavel', 2:'alimentacao e bebida', 3:'valor'})
    alimentacao_bebidas = alimentacao_bebidas.groupby(alimentacao_bebidas['data'].dt.strftime('%Y-%m')).mean()['valor'].to_frame().rename(columns={'valor':'alimentacao_bebidas'})
  if numero == 2:
    numero_str = str(numero) + '.'
    linhas_com_2 = ipca_analise.loc[ipca_analise['grupo'].str.startswith(numero_str)]
    lista = linhas_com_2.values.tolist()
    todas_listas.append(lista)
    habitacao = pd.concat([pd.DataFrame(lista) for lista in todas_listas], ignore_index=True).rename(columns = {0: 'data', 1:'variavel', 2:'habitacao', 3:'valor'})
    habitacao = habitacao.groupby(habitacao['data'].dt.strftime('%Y-%m')).mean()['valor'].to_frame().rename(columns={'valor':'habitacao'})
  if numero == 3:
    numero_str = str(numero) + '.'
    linhas_com_3 = ipca_analise.loc[ipca_analise['grupo'].str.startswith(numero_str)]
    lista = linhas_com_3.values.tolist()
    todas_listas.append(lista)
    artigos_residencia = pd.concat([pd.DataFrame(lista) for lista in todas_listas], ignore_index=True).rename(columns = {0: 'data', 1:'variavel', 2:'artigos de residencia', 3:'valor'})
    artigos_residencia = artigos_residencia.groupby(artigos_residencia['data'].dt.strftime('%Y-%m')).mean()['valor'].to_frame().rename(columns={'valor':'artigos_residencia'})
  if numero == 4:
    numero_str = str(numero) + '.'
    linhas_com_4 = ipca_analise.loc[ipca_analise['grupo'].str.startswith(numero_str)]
    lista = linhas_com_4.values.tolist()
    todas_listas.append(lista)
    vestuario = pd.concat([pd.DataFrame(lista) for lista in todas_listas], ignore_index=True).rename(columns = {0: 'data', 1:'variavel', 2:'vestuario', 3:'valor'})
    vestuario = vestuario.groupby(vestuario['data'].dt.strftime('%Y-%m')).mean()['valor'].to_frame().rename(columns={'valor':'vestuario'})
  if numero == 5:
    numero_str = str(numero) + '.'
    linhas_com_5 = ipca_analise.loc[ipca_analise['grupo'].str.startswith(numero_str)]
    lista = linhas_com_5.values.tolist()
    todas_listas.append(lista)
    transportes = pd.concat([pd.DataFrame(lista) for lista in todas_listas], ignore_index=True).rename(columns = {0: 'data', 1:'variavel', 2:'trasportes', 3:'valor'})
    transportes = transportes.groupby(transportes['data'].dt.strftime('%Y-%m')).mean()['valor'].to_frame().rename(columns={'valor':'transportes'})
  if numero == 6:
    numero_str = str(numero) + '.'
    linhas_com_6 = ipca_analise.loc[ipca_analise['grupo'].str.startswith(numero_str)]
    lista = linhas_com_6.values.tolist()
    todas_listas.append(lista)
    saude = pd.concat([pd.DataFrame(lista) for lista in todas_listas], ignore_index=True).rename(columns = {0: 'data', 1:'variavel', 2:'saude e cuidados pessoais', 3:'valor'})
    saude = saude.groupby(saude['data'].dt.strftime('%Y-%m')).mean()['valor'].to_frame().rename(columns={'valor':'saude'})
  if numero == 7:
    numero_str = str(numero) + '.'
    linhas_com_7 = ipca_analise.loc[ipca_analise['grupo'].str.startswith(numero_str)]
    lista = linhas_com_7.values.tolist()
    todas_listas.append(lista)
    despesas_pessoais = pd.concat([pd.DataFrame(lista) for lista in todas_listas], ignore_index=True).rename(columns = {0: 'data', 1:'variavel', 2:'despesas pessoais', 3:'valor'})
    despesas_pessoais = despesas_pessoais.groupby(despesas_pessoais['data'].dt.strftime('%Y-%m')).mean()['valor'].to_frame().rename(columns={'valor':'despesas_pessoais'})
  if numero == 8:
    numero_str = str(numero) + '.'
    linhas_com_8 = ipca_analise.loc[ipca_analise['grupo'].str.startswith(numero_str)]
    lista = linhas_com_8.values.tolist()
    todas_listas.append(lista)
    educacao = pd.concat([pd.DataFrame(lista) for lista in todas_listas], ignore_index=True).rename(columns = {0: 'data', 1:'variavel', 2:'educacao', 3:'valor'})
    educacao = educacao.groupby(educacao['data'].dt.strftime('%Y-%m')).mean()['valor'].to_frame().rename(columns={'valor':'educacao'})        
  if numero == 9:
    numero_str = str(numero) + '.'
    linhas_com_9 = ipca_analise.loc[ipca_analise['grupo'].str.startswith(numero_str)]
    lista = linhas_com_9.values.tolist()
    todas_listas.append(lista)
    comunicacao = pd.concat([pd.DataFrame(lista) for lista in todas_listas], ignore_index=True).rename(columns = {0: 'data', 1:'variavel', 2:'comunicacao', 3:'valor'})
    comunicacao = comunicacao.groupby(comunicacao['data'].dt.strftime('%Y-%m')).mean()['valor'].to_frame().rename(columns={'valor':'comunicacao'})

df_geral_ipca = pd.concat([alimentacao_bebidas, habitacao, artigos_residencia, vestuario, transportes, saude, despesas_pessoais, educacao, comunicacao], axis =1)

indice_geral = ipca_analise.query('grupo == "Índice geral"')
indice_geral = indice_geral.groupby(indice_geral['data'].dt.strftime('%Y-%m')).mean()['valor'].to_frame()

#Gráfico é no Gold 
fig = go.Figure()
fig.add_trace(go.Scatter(x = indice_geral.index, y = indice_geral['valor'], name= 'Índice Geral', line=dict(color='black')))
fig.add_trace(go.Scatter(x = df_geral_ipca.index, y = df_geral_ipca['alimentacao_bebidas'], name= 'Alimentação/bebidas'))
fig.add_trace(go.Scatter(x = df_geral_ipca.index, y = df_geral_ipca['habitacao'], name= 'Habitação'))
fig.add_trace(go.Scatter(x = df_geral_ipca.index, y = df_geral_ipca['artigos_residencia'], name= 'Artigos de residência'))
fig.add_trace(go.Scatter(x = df_geral_ipca.index, y = df_geral_ipca['vestuario'], name= 'Vestuário'))
fig.add_trace(go.Scatter(x = df_geral_ipca.index, y = df_geral_ipca['transportes'], name= 'Transportes'))
fig.add_trace(go.Scatter(x = df_geral_ipca.index, y = df_geral_ipca['saude'], name= 'Saúde'))
fig.add_trace(go.Scatter(x = df_geral_ipca.index, y = df_geral_ipca['despesas_pessoais'], name= 'Despesas Pessoais'))
fig.add_trace(go.Scatter(x = df_geral_ipca.index, y = df_geral_ipca['educacao'], name= 'Educação'))
fig.add_trace(go.Scatter(x = df_geral_ipca.index, y = df_geral_ipca['comunicacao'], name= 'Comunicação'))
fig.update_layout(title_text = 'Grupos do IPCA mensal')
fig.show()

