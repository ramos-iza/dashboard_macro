import main_silver
import plotly.graph_objects as go 


merge_2022 = main_silver.merge_2022()
merge_2022 = merge_2022

fig = go.Figure()
fig.add_trace(go.Scatter(x = merge_2022.index, y = merge_2022['Mediana'], name = 'exp IPCA 2022'))
fig.add_trace(go.Scatter(x = merge_2022.index, y = merge_2022[2022], name = 'IPCA 2022'))
fig.show()

indice_geral = main_silver.indice_geral()
indice_geral = indice_geral.reset_index() 

df_geral_ipca = main_silver.df_geral_ipca()
geral_ipca_df = df_geral_ipca

fig = go.Figure()
fig.add_trace(go.Scatter(x = indice_geral['data'], y = indice_geral['valor'], name= 'Índice Geral', line=dict(color='black')))
fig.add_trace(go.Scatter(x = geral_ipca_df.index, y = geral_ipca_df['alimentacao_bebidas'], name= 'Alimentação/bebidas'))
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