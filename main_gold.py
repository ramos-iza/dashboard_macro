import plotly.graph_objects as go 
import config 
import gold_data.read_data as rd
import silver_data.save_silver_data as ssd
import plotly.graph_objects as go 
import plotly.express as px
import matplotlib
#import config 
import pandas as pd 
from plotly.subplots import make_subplots
from config import silver as config_silver
from config import raw as config_raw

def run_gold(config_silver, config_raw):
    print('----- IPCA -----')

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

    # Para o primeiro gráfico - IPCA mensal e acumulado 
    ipca_mes = rd.read_csv(config.silver['ipca_mes']['save_path'])
    ipca_acum_12m = rd.read_csv(config.silver['ipca_acum_12m']['save_path'])
    ipca_acum_12m['data'] = pd.to_datetime(ipca_acum_12m['data'])


    fig = go.Figure()
    fig.add_trace(go.Bar(x= ipca_mes['data'], y =ipca_mes['V']))
    fig.add_trace(go.Bar(x=ipca_acum_12m['data'], y=ipca_acum_12m['ipca_acum_ano']))
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

    # Emprego 

    # Taxa de desemprego
    db_taxa_desemprego = rd.read_csv(config.silver['db_taxa_desemprego']['save_path'])

    fig = px.line(db_taxa_desemprego, y=db_taxa_desemprego['Valor'], x=db_taxa_desemprego['Trimestre Móvel'])
    fig.show()

    # variacao por tipo de emprego
    var_percent_tipo_emprego = rd.read_csv(config.silver['var_percent_tipo_emprego']['save_path'])

    fig = px.line(var_percent_tipo_emprego, x='Trimestre Móvel', y='Valor', color='Posição na ocupação e categoria do emprego no trabalho principal',
                title='Gráfico de Linhas por Categoria de Emprego')
    fig.update_layout(xaxis_title='Trimestre Móvel', yaxis_title='Valor')

    fig.show()

    #Pivot
    pivot_var_percent_tipo_empreg = rd.read_csv(config.silver['pivot_var_percent_tipo_empreg']['save_path'])

    # Grandes regioes 
    db_grandes_regioes = rd.read_csv(config.silver['db_grandes_regioes']['save_path'])

    fig = px.line(db_grandes_regioes, x='Trimestre', y='Valor', color='Grande Região',
                title='Taxa de desocupacao das pessoas com 14 anos o mais de idade, na semana de referencia (em %) - Grandes regioes ')
    fig.update_layout(xaxis_title='Trimestre', yaxis_title='Valor')
    fig.show()

    # Sexo
    db_desempre_sexo = rd.read_csv(config.silver['db_desempre_sexo']['save_path'])
    merge_homem_mulher = rd.read_csv(config.silver['merge_homem_mulher']['save_path'])

    fig = px.line(db_desempre_sexo, x='Trimestre', y='Valor', color='Sexo',
                title='Taxa de desocupacao das pessoas de 14 anos ou mais, na semana de refernecia, por sexo (%)')
    fig.update_layout(xaxis_title='Trimestre', yaxis_title='Valor')
    fig.update_layout(yaxis2=dict(title='', overlaying='y', side='right'))
    fig.add_scatter(x=merge_homem_mulher['Trimestre'], y=merge_homem_mulher['diferenca'], 
                    fill='tozeroy', mode='lines', name='Diferença percentual entre homens e mulheres', yaxis='y2')
    fig.show()   

    # Por idade 
    db_pop_idade = rd.read_csv(config.silver['db_pop_idade']['save_path'])

    fig = px.line(db_pop_idade, x='Trimestre', y='Valor', color='Grupo de idade',
                title='Taxa de desocupação, por idade, 1º trimestre 2012 - 2º trimestre 2023')

    fig.update_layout(xaxis_title='Trimestre', yaxis_title='Valor')
    fig.show()

    # Rendimento regiao  
    rendimento_regiao_1 = rd.read_csv(config.silver['rendimento_regiao_1']['save_path'])

    fig = px.line(rendimento_regiao_1, x='Trimestre', y='Valor', color='Grandes Regiões',
                title='Rendimento Médio, por grande região, 1º trimestre 2012 - 2º trimestre 2023')
    fig.update_layout(xaxis_title='Trimestre', yaxis_title='Valor')
    fig.show()

    # Rendimento idade 
    rendimento_idade = rd.read_csv(config.silver['rendimento_idade']['save_path'])

    fig = px.line(rendimento_idade, x='Trimestre', y='Valor', color='Grupo de idade',
                title='Rendimento Médio, por idade, 1º trimestre 2012 - 2º trimestre 2023')
    fig.update_layout(xaxis_title='Trimestre', yaxis_title='Valor')
    fig.show()

    # Caged 
    dados_caged = rd.read_csv(config.silver['dados_caged']['save_path'])

    bar_admissoes = go.Bar(
        x=dados_caged['data'],
        y=dados_caged['admissoes'],
        name='Admissões',
        marker=dict(color='#ccdcff')
    )

    # Crie um objeto Bar para 'demissoes'
    bar_demissoes = go.Bar(
        x=dados_caged['data'],
        y=dados_caged['demissoes'],
        name='Demissões',
        marker=dict(color='#dcdcdc')
    )

    # Crie um objeto Scatter para 'saldo' com o eixo y secundário
    scatter_saldo = go.Scatter(
        x=dados_caged['data'],
        y=dados_caged['saldo'],
        name='Saldo',
        mode='lines',
        #yaxis='y2',
        line=dict(color='#ff8247')
    )

    # Crie o layout do gráfico com dois eixos y e fundo branco
    layout = go.Layout(
        title='Admissões, Demissões e Saldo no CAGED',
        xaxis=dict(title='Trimestre'),
        yaxis=dict(title='Admissões e Demissões'),
        yaxis2=dict(
            title='Saldo',
            overlaying='y',
            side='right'
        ),
        plot_bgcolor='white'  # Defina o fundo como branco
    )

    # Crie a figura com os objetos Bar e Scatter e o layout
    fig = go.Figure(data=[bar_admissoes, bar_demissoes, scatter_saldo], layout=layout)

    # Exiba o gráfico
    fig.show()


    # Credito 
    dados_credito = rd.read_csv(config.silver['dados_credito']['save_path'])
    ipca_credito = rd.read_csv(config.silver['ipca_credito']['save_path'])
    concessoes = rd.read_csv(config.silver['concessoes']['save_path'])

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dados_credito["Concessões de crédito - Total"].index, y=dados_credito["Concessões de crédito - Total"] / 1000, mode='lines'))
    fig.update_layout(title='"Concessões de crédito - Total\nValores nominais\nDados: BCB"', yaxis_title="R$ bilhões")
    fig.show()

    fig = make_subplots(rows=2, cols=2)
    fig.add_trace(go.Scatter(x=dados_credito['data'], y=dados_credito["Concessões de crédito - PF"] / 1000, mode='lines', name='Concessões de crédito - PF'), row=1, col=1)
    fig.add_trace(go.Scatter(x=dados_credito['data'], y=dados_credito["Concessões de crédito - PJ"] / 1000, mode='lines', name='Concessões de crédito - PJ'), row=1, col=2)
    fig.add_trace(go.Scatter(x=dados_credito['data'], y=dados_credito["Concessões de crédito - Livre"] / 1000, mode='lines', name='Concessões de crédito - Livre'), row=2, col=1)
    fig.add_trace(go.Scatter(x=dados_credito['data'], y=dados_credito["Concessões de crédito - Direcionado"] / 1000, mode='lines', name='Concessões de crédito - Direcionado'), row=2, col=2)
    fig.update_layout(
        title='Concessões de crédito\nValores nominais',
        yaxis_title="R$ bilhões",
        width=1000,  # Largura total do gráfico
        height=600,   # Altura total do gráfico
    )
    fig.show()

    data_atual = concessoes['data'] = pd.to_datetime(concessoes['data'])
    data_atual = concessoes.tail(1)["data"].dt.strftime("%b/%Y").item()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=concessoes["data"], y=concessoes["ajuste"], mode='lines'))
    fig.update_layout(title=f"Concessões de crédito - Total<br>Valores deflacionados pelo IPCA a preços de {data_atual} e ajustado sazonalmente pelo X13-SEATS-ARIMA.", 
                    yaxis_title="R$ bilhões")
    fig.show()

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dados_credito["data"], y=dados_credito["Saldo da carteira de crédito - Total"] / dados_credito["PIB acumulado dos últimos 12 meses"] * 100, fill='tozeroy', mode='none'))
    fig.update_layout(title=f"Estoque de Crédito", 
                    yaxis_title="R$ bilhões")
    fig.show()

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dados_credito["data"], y=dados_credito["Saldo da carteira de crédito - Total"] / dados_credito["PIB acumulado dos últimos 12 meses"] * 100, fill='tozeroy', mode='none'))
    fig.update_layout(title=f"Estoque de Crédito", 
                    yaxis_title="R$ bilhões")
    fig.show()

    dados_credito = dados_credito.set_index('data')
    x = dados_credito.index
    y_privado = dados_credito["Saldos de crédito - Privado"] / dados_credito["Saldo da carteira de crédito - Total"] * 100
    y_publico = dados_credito["Saldos de crédito - Público"] / dados_credito["Saldo da carteira de crédito - Total"] * 100
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y_privado, fill='tozeroy', mode='none', name='Privado', stackgroup='stack'))
    fig.add_trace(go.Scatter(x=x, y=y_publico, fill='tozeroy', mode='none', name='Público', stackgroup='stack'))
    fig.update_layout(title=f"Estoque de Crédito",
                    yaxis_title="% Total", 
                    legend_title="Categorias")
    fig.show()


    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dados_credito.index, y=dados_credito["Taxa média de juros das operações de crédito"], mode='lines'))
    fig.update_layout(title=f"Taxa de juros - Mercado de Crédito - Brasil", 
                    yaxis_title="% a.a.")
    fig.show()


    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dados_credito.index, y=dados_credito["Spread médio das operações de crédito"], mode='lines'))
    fig.update_layout(title=f"Spread bancário - Mercado de Crédito - Brasil", 
                    yaxis_title="p.p.")
    fig.show()

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dados_credito.index, y=dados_credito["Inadimplência da carteira de crédito"], mode='lines'))
    fig.update_layout(title=f"Inadimplência - Mercado de Crédito - Brasil", 
                    yaxis_title="p.p.")
    fig.show()

    x = dados_credito.index
    y_pf = dados_credito["Concessões de crédito - PF"] / dados_credito["Concessões de crédito - Total"] * 100
    y_pj = dados_credito["Concessões de crédito - PJ"] / dados_credito["Concessões de crédito - Total"] * 100
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y_pf, fill='tozeroy', mode='none', name='Pf', stackgroup='stack'))
    fig.add_trace(go.Scatter(x=x, y=y_pj, fill='tozeroy', mode='none', name='Pj', stackgroup='stack'))
    fig.update_layout(title=f"Concessão de crédito PF x PJ",
                    yaxis_title="% Total", 
                    legend_title="Categorias")
    fig.show()

if __name__ == '__main__':
    run_gold(
        config_silver=config_silver,
        config_raw=config_raw,
        )