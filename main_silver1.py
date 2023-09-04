import config 
import pandas as pd 
import silver_data.read_silver_data as rd
import silver_data.transform_silver as ts
import silver_data.save_silver_data as ssd
import datetime
from ast import Assign
import plotly.graph_objects as go 
import plotly.express as px


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
'''proporcao = ts.calc_proporcao(df_geral_ipca=df_geral_ipca)
#save
ssd.save_csv(
    df=proporcao, 
    path=config.silver['proporcao']['save_path']
)'''

'''  
fig = go.Figure(data=[go.Pie(labels=proporcao[0], values=proporcao[1])])
fig.update_layout(title_text='Coparação das variações dos grupos do IPCA - 03/2023')
fig.show()'''

#IPCA ao ano por região metropolitana
#read
ipca_rm = rd.ler_csv(config.raw['ipca_rm']['path'])
#Transform
ipca_rm = ts.trasform_ipca_rm(ipca_rm=ipca_rm)
#save 
ssd.save_csv(
    df=ipca_rm, 
    path=config.silver['ipca_rm']['save_path']
)
'''Gold
import plotly.express as px

fig = px.bar(ipca_rm, x='ano', y='valor', color='Região Metropolitana', barmode='group')
fig.update_layout(title_text = 'IPCA - Variação acumulada no ano', xaxis={'type':'category'})
fig.show()'''

#Silver IPCA núcleo
#read
ipca_nucleo = rd.ler_csv(config.raw['ipca_nucleo']['path'])
#transform
nucleo_long = ts.calc_nucleos_ipca(ipca_nucleo=ipca_nucleo)
#save
ssd.save_csv(
    df= nucleo_long, 
    path= config.silver['nucleo_long']['save_path']
)

'''
import plotly.express as px
fig = px.bar(nucleo_long, x='Date', y= 'valor', color='Núcleos', barmode='group')
fig.update_layout(title_text = 'Núcleos do IPCA', xaxis={'type' : 'category'})
fig.show()'''

'''gold
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
)'''

#Comparar a médias dos núcleos com o IPCA histórico
#transform
nucleo_ipca_merge = ts.calc_comp_media_nucleos(ipca_nucleo=ipca_nucleo, ipca_anual=ipca_anual)
#save
ssd.save_csv(
    df=nucleo_ipca_merge,
    path= config.silver['nucleo_ipca_merge']['save_path']
)


'''
fig = go.Figure()
fig.add_trace(go.Scatter(x= nucleo_ipca_merge.index, y= nucleo_ipca_merge['media'], name='Média dos núcleos'))
fig.add_trace(go.Scatter(x= nucleo_ipca_merge.index, y= nucleo_ipca_merge['ipca_anual'], name='IPCA Anual'))
fig.update_layout(title_text='Média dos núcleos x IPCA')
fig.show()'''

#IPCA mensal x IPCA acum 12m
#read
dados_brutos_ipca_sidra = rd.ler_csv(config.raw['dados_brutos_ipca_sidra']['path'])
#transform
ipca_analise_novo = ts.calc_p_nova_analise(dados_brutos_ipca_sidra=dados_brutos_ipca_sidra)
vm_grupos = ts.calc_valor_mensal(ipca_analise_novo=ipca_analise_novo)
ipca_acum_ano = ts.calc_ipca_acum_ano(ipca_analise_novo=ipca_analise_novo)
tabela = ts.juntando_tab(vm_grupos=vm_grupos)
tabela_acum_mes_corrente = ts.calc_acum_corrente(ipca_acum_ano=ipca_acum_ano, tabela=tabela)
peso_mensal_corrente = ts.trat_peso_mensal_corrente(tabela)
juntos = ts.juntando_ipca_corrente(tabela_acum_mes_corrente=tabela_acum_mes_corrente, peso_mensal_corrente=peso_mensal_corrente)

ultima_data = ts.last_date(dados_brutos_ipca_sidra=dados_brutos_ipca_sidra)

#save
ssd.save_csv(
    df= ipca_analise_novo,
    path= config.silver['ipca_analise_novo']['save_path']
)

ssd.save_csv(
    df= vm_grupos,
    path= config.silver['vm_grupos']['save_path']
)

ssd.save_csv(
    df= ipca_acum_ano,
    path= config.silver['ipca_acum_ano']['save_path']
)

ssd.save_csv(
    df= tabela,
    path= config.silver['tabela']['save_path']
)

ssd.save_csv(
    df= tabela_acum_mes_corrente,
    path= config.silver['tabela_acum_corrente']['save_path']
)

ssd.save_csv(
    df= peso_mensal_corrente,
    path= config.silver['peso_mensal_corrente']['save_path']
)

ssd.save_csv(
    df= juntos,
    path= config.silver['juntos']['save_path']
)


''' Gold
fig = go.Figure()
fig.add_trace(go.Bar(x = juntos['valor_y'], y = juntos['grupo'], name = 'Variação acumulada ao ano', orientation='h'))
fig.add_trace(go.Bar(x = juntos['valor_x'], y = juntos['grupo'], name = 'Variação mensal', orientation='h'))
fig.update_layout(title_text = 'IPCA - Variação mensal e acumulada no ano (%) - Índice geral e grupos de produtos e serviços - Brasil - abril 2023')
fig.update_yaxes(categoryorder='category descending')
fig.show()'''

# Pib 

# Read
pib_volume_trimestral = rd.read_csv(config.raw['pib_volume_trimestral']['path'])

# Transform
dados_margem = ts.calc_dados_margem(pib_volume_trimestral=pib_volume_trimestral)

dados_margem = ts.col_trimestre(dados_margem = dados_margem)

taxas = ts.calc_taxa_var(dados_margem = dados_margem)

taxas = ts.calc_variacao_interanual(taxas=taxas)

data = ts.filtrando_pib(taxas=taxas)

# save
ssd.save_csv(
    df= data,
    path= config.silver['data']['save_path']
)

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

#Pib sazional 

# Read
db_trimestre_sazional = rd.read_csv(config.raw['db_trimestre_sazional']['path'])

db_trimestre_sazional = ts.calc_pib_tri_sazional(db_trimestre_sazional=db_trimestre_sazional)

taxas1 = ts.calc_taxa_var_sazional(db_trimestre_sazional=db_trimestre_sazional)

data1 = ts.colum_taxa_var(taxas1=taxas1)

data1 = ts.formatando_data(taxas1=taxas1)

data1 = ts.col_trimestre1(data1=data1)

# Save 
ssd.save_csv(
    df= data1,
    path= config.silver['data1']['save_path'])

fig = px.bar(
    data1,
    x="trimestre",
    y="Var. % margem",
    labels={"value": "Variação (%)"},
    title="PIB: Série encadeada do índice de volume trimestral com ajuste sazonal",
    template="plotly",
)

fig.show()