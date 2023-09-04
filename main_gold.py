import plotly.graph_objects as go 
import config 
import gold_data.read_data as rd
import silver_data.save_silver_data as ssd
import plotly.graph_objects as go 
import plotly.express as px
import matplotlib
import config 

#IPCA Focus

dataframe_2019 = rd.read_csv(config.silver['dataframe_2019']['save_path'])

fig = go.Figure()
fig.add_trace(go.Scatter(x = dataframe_2019.index, y = dataframe_2019['Mediana'], name = 'exp IPCA 2019'))
fig.add_trace(go.Scatter(x = dataframe_2019.index, y = dataframe_2019['ipca_anual'], name = 'IPCA 2019'))
fig.show()

dataframe_2020 = rd.read_csv(config.silver['dataframe_2020']['save_path'])

fig = go.Figure()
fig.add_trace(go.Scatter(x = dataframe_2020.index, y = dataframe_2020['Mediana'], name = 'exp IPCA 2020'))
fig.add_trace(go.Scatter(x = dataframe_2020.index, y = dataframe_2020['ipca_anual'], name = 'IPCA 2020'))
fig.show()

dataframe_2021 = rd.read_csv(config.silver['dataframe_2021']['save_path'])

fig = go.Figure()
fig.add_trace(go.Scatter(x = dataframe_2021.index, y = dataframe_2021['Mediana'], name = 'exp IPCA 2021'))
fig.add_trace(go.Scatter(x = dataframe_2021.index, y = dataframe_2021['ipca_anual'], name = 'IPCA 2021'))
fig.show()

dataframe_2022 = rd.read_csv(config.silver['dataframe_2022']['save_path'])

fig = go.Figure()
fig.add_trace(go.Scatter(x = dataframe_2022.index, y = dataframe_2022['Mediana'], name = 'exp IPCA 2022'))
fig.add_trace(go.Scatter(x = dataframe_2022.index, y = dataframe_2022['ipca_anual'], name = 'IPCA 2022'))
fig.show()

dataframe_2023 = rd.read_csv(config.silver['dataframe_2023']['save_path'])

fig = go.Figure()
fig.add_trace(go.Scatter(x = dataframe_2023.index, y = dataframe_2023['Mediana'], name = 'exp IPCA 2023'))
fig.add_trace(go.Scatter(x = dataframe_2023.index, y = dataframe_2023['ipca_anual'], name = 'IPCA 2023'))
fig.show()

# Grupos IPCA
df_geral_ipca = rd.read_csv(config.silver['df_geral_ipca']['save_path'])
indice_geral = rd.read_csv(config.silver['indice_geral']['save_path'])

grupos_ipca = (df_geral_ipca.set_index('data')).columns

fig = go.Figure()
indice_geral_data = indice_geral.reset_index()
fig.add_trace(go.Scatter(x = indice_geral['data'], y = indice_geral['valor'], name= 'Índice Geral', line=dict(color='black')))
fig.add_trace(go.Scatter(x = df_geral_ipca.data, y = df_geral_ipca['Alimentação e bebidas'], name= 'Alimentação/bebidas'))
fig.add_trace(go.Scatter(x = df_geral_ipca.data, y = df_geral_ipca['Habitação'], name= 'Habitação'))
fig.add_trace(go.Scatter(x = df_geral_ipca.data, y = df_geral_ipca['Artigos de residência'], name= 'Artigos de residência'))
fig.add_trace(go.Scatter(x = df_geral_ipca.data, y = df_geral_ipca['Vestuário'], name= 'Vestuário'))
fig.add_trace(go.Scatter(x = df_geral_ipca.data, y = df_geral_ipca['Transportes'], name= 'Transportes'))
fig.add_trace(go.Scatter(x = df_geral_ipca.data, y = df_geral_ipca['Saúde'], name= 'Saúde'))
fig.add_trace(go.Scatter(x = df_geral_ipca.data, y = df_geral_ipca['Despesas Pessoais'], name= 'Despesas Pessoais'))
fig.add_trace(go.Scatter(x = df_geral_ipca.data, y = df_geral_ipca['Educação'], name= 'Educação'))
fig.add_trace(go.Scatter(x = df_geral_ipca.data, y = df_geral_ipca['Comunicação'], name= 'Comunicação'))
fig.update_layout(title_text = 'Grupos do IPCA mensal')
fig.show()


#Proporcão
proporcao = rd.read_csv(config.silver['proporcao']['save_path'])

fig = go.Figure(data=[go.Pie(labels=proporcao['Unnamed: 0'], values=proporcao['proporcao'])])
fig.update_layout(title_text='Coparação das variações dos grupos do IPCA - 03/2023')
fig.show()

#IPCA ao ano por região metropolitana
ipca_rm = rd.read_csv(config.silver['ipca_rm']['save_path'])

fig = px.bar(ipca_rm, x='ano', y='valor', color='Região Metropolitana', barmode='group')
fig.update_layout(title_text = 'IPCA - Variação acumulada no ano', xaxis={'type':'category'})
fig.show()


#Silver IPCA núcleo
nucleo_long= rd.read_csv(config.silver['nucleo_long']['save_path'])
ipca_nucleo = rd.read_csv(config.raw['ipca_nucleo']['path'])

fig = px.bar(nucleo_long, x='Date', y= 'valor', color='Núcleos', barmode='group')
fig.update_layout(title_text = 'Núcleos do IPCA', xaxis={'type' : 'category'})
fig.show()

import matplotlib
(
    ipca_nucleo
    .rolling(window = 12)
    .apply(lambda x: ((x / 100 + 1).prod() - 1) * 100, raw = False)
    .plot(
        subplots = True,
        figsize = (25,10),
        layout = (2,4),
        title = 'Núcleos IPCA',
        xlabel = ''
        )
)    

#Comparar a médias dos núcleos com o IPCA histórico
nucleo_ipca_merge = rd.read_csv(config.silver['nucleo_ipca_merge']['save_path'])

fig = go.Figure()
fig.add_trace(go.Scatter(x= nucleo_ipca_merge.index, y= nucleo_ipca_merge['media'], name='Média dos núcleos'))
fig.add_trace(go.Scatter(x= nucleo_ipca_merge.index, y= nucleo_ipca_merge['ipca_anual'], name='IPCA Anual'))
fig.update_layout(title_text='Média dos núcleos x IPCA')
fig.show()

#IPCA mensal x IPCA acum 12m
juntos = rd.read_csv(config.silver['juntos']['save_path'])

fig = go.Figure()
fig.add_trace(go.Bar(x = juntos['valor_y'], y = juntos['grupo'], name = 'Variação acumulada ao ano', orientation='h'))
fig.add_trace(go.Bar(x = juntos['valor_x'], y = juntos['grupo'], name = 'Variação mensal', orientation='h'))
fig.update_layout(title_text = 'IPCA - Variação mensal e acumulada no ano (%) - Índice geral e grupos de produtos e serviços - Brasil - maio 2023')
fig.update_yaxes(categoryorder='category descending')
fig.show()


# PIB 
data = rd.read_csv(config.silver['data']['save_path'])

fig = px.bar(
    data,
    x="trimestre",
    y='Var. % interanual',
    labels={"value": "Variação (%)"},
    title="PIB: Taxas de Variação Interanual",
    template="plotly",
)
fig.show()

fig = px.bar(
    data,
    x="trimestre",
    y='Var. % anual',
    labels={"value": "Variação (%)"},
    title="PIB: Taxas de Variação Anual",
    template="plotly",
)
fig.show()

#Trimestre / mesmo trimestre do ano anterior
fig = px.bar(
    data,
    x="trimestre",
    y='Var. % acumulada no ano',
    labels={"value": "Var. % acumulada no ano"}, 
    title="PIB: Var. % acumulada no ano", 
    template="plotly",
)

fig.show()

# Pib ajuste sazional 
data1 = rd.read_csv(config.silver['data1']['save_path'])

fig = px.bar(
    data1,
    x="trimestre",
    y="Var. % margem",
    labels={"value": "Variação (%)"},
    title="PIB: Série encadeada do índice de volume trimestral com ajuste sazonal",
    template="plotly",
)

fig.show()


