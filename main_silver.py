from config import silver as config_silver
from config import raw as config_raw
import pandas as pd 
import silver_data.read_silver_data as rd
import silver_data.transform_silver as ts
import silver_data.save_silver_data as ssd
import datetime
from ast import Assign
import plotly.graph_objects as go 
import plotly.express as px
from statsmodels.tsa import x13
import os


def run_silver(config_silver, config_raw, show_plots=False):
    print('----- IPCA -----')
    #Calc IPCA Anual
    # Read
    ipca_mensal = rd.read_csv(config_silver['ipca_anual']['read_path'])
    # Transform
    ipca_anual = ts.calc_ipca_anual(ipca_mensal)
    # Save
    ssd.save_csv(
    df=ipca_anual, 
    path=config_silver['ipca_anual']['save_path']
    )

    #IPCA Focus
    #Read
    ipca_anual = rd.read_csv(config_silver['ipca_anual']['save_path'])
    ipca_focus = rd.read_csv(config_silver['ipca_focus']['read_path'])
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
        path=config_silver['ipca_focus']['save_path']    
    )
    ssd.save_csv(
        df=dataframe_2019, 
        path=config_silver['dataframe_2019']['save_path']
    )

    ssd.save_csv(
        df=dataframe_2020, 
        path=config_silver['dataframe_2020']['save_path']
    )

    ssd.save_csv(
        df=dataframe_2021, 
        path=config_silver['dataframe_2021']['save_path']
    )

    ssd.save_csv(
        df=dataframe_2022, 
        path=config_silver['dataframe_2022']['save_path']
    )
    ssd.save_csv(
        df=dataframe_2023, 
        path=config_silver['dataframe_2023']['save_path']
    )


    #Grupos IPCA 
    #read
    dados_brutos_ipca_sidra = rd.ler_csv(config_raw['dados_brutos_ipca_sidra']['path'])
    #Transform
    ipca_analise = ts.trat_grupo_ipca(dados_brutos_ipca_sidra=dados_brutos_ipca_sidra)
    df_geral_ipca = ts.cal_df_geral_ipca(ipca_analise=ipca_analise)
    indice_geral = ts.indice_geral(ipca_analise=ipca_analise)
    #save
    
    ssd.save_csv(
        df=ipca_analise,
        path=config_silver['ipca_analise']['save_path']
    )

    ssd.save_csv(
        df=df_geral_ipca, 
        path=config_silver['df_geral_ipca']['save_path']
    )

    ssd.save_csv(
        df=indice_geral, 
        path=config_silver['indice_geral']['save_path']
    )


    #Proporcão
    #Transform 
    
    #IPCA ao ano por região metropolitana
    #read
    ipca_rm = rd.ler_csv(config_raw['ipca_rm']['path'])
    #Transform
    ipca_rm = ts.trasform_ipca_rm(ipca_rm=ipca_rm)
    #save 
    ssd.save_csv(
        df=ipca_rm, 
        path=config_silver['ipca_rm']['save_path']
    )

    #Silver IPCA núcleo
    #read
    ipca_nucleo = rd.ler_csv(config_raw['ipca_nucleo']['path'])
    #transform
    nucleo_long = ts.calc_nucleos_ipca(ipca_nucleo=ipca_nucleo)
    #save
    ssd.save_csv(
        df= nucleo_long, 
        path= config_silver['nucleo_long']['save_path']
    )

    #Comparar a médias dos núcleos com o IPCA histórico
    #transform
    nucleo_ipca_merge = ts.calc_comp_media_nucleos(ipca_nucleo=ipca_nucleo, ipca_anual=ipca_anual)
    #save
    ssd.save_csv(
        df=nucleo_ipca_merge,
        path= config_silver['nucleo_ipca_merge']['save_path']
    )


    #IPCA mensal x IPCA acum 12m
    #read
    dados_brutos_ipca_sidra = rd.ler_csv(config_raw['dados_brutos_ipca_sidra']['path'])
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
        path= config_silver['ipca_analise_novo']['save_path']
    )

    ssd.save_csv(
        df= vm_grupos,
        path= config_silver['vm_grupos']['save_path']
    )

    ssd.save_csv(
        df= ipca_acum_ano,
        path= config_silver['ipca_acum_ano']['save_path']
    )

    ssd.save_csv(
        df= tabela,
        path= config_silver['tabela']['save_path']
    )

    ssd.save_csv(
        df= tabela_acum_mes_corrente,
        path= config_silver['tabela_acum_corrente']['save_path']
    )

    ssd.save_csv(
        df= peso_mensal_corrente,
        path= config_silver['peso_mensal_corrente']['save_path']
    )

    ssd.save_csv(
        df= juntos,
        path= config_silver['juntos']['save_path']
    )

    # Para o primeiro gráfico - IPCA mensal e acumulado 
    #Transform 
    ipca_mes = ts.calc_ipca_mes(dados_brutos_ipca_sidra=dados_brutos_ipca_sidra)
    ipca_acum_12m = ts.calc_ipca_12m(ipca_acum_ano=ipca_acum_ano)

    # save
    ssd.save_csv(
        df= ipca_mes,
        path= config_silver['ipca_mes']['save_path']
    )

    ssd.save_csv(
        df= ipca_acum_12m,
        path= config_silver['ipca_acum_12m']['save_path']
    )

    # Pib 
    print('----- PIB -----')
    # Read
    pib_volume_trimestral = rd.read_csv(config_raw['pib_volume_trimestral']['path'])

    # Transform
    dados_margem = ts.calc_dados_margem(pib_volume_trimestral=pib_volume_trimestral)

    dados_margem = ts.col_trimestre(dados_margem = dados_margem)

    taxas = ts.calc_taxa_var(dados_margem = dados_margem)

    taxas = ts.calc_variacao_interanual(taxas=taxas)

    data = ts.filtrando_pib(taxas=taxas)

    # save
    ssd.save_csv(
        df= data,
        path= config_silver['data']['save_path']
    )

    if show_plots:
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
    db_trimestre_sazional = rd.read_csv(config_raw['db_trimestre_sazional']['path'])

    db_trimestre_sazional = ts.calc_pib_tri_sazional(db_trimestre_sazional=db_trimestre_sazional)

    taxas1 = ts.calc_taxa_var_sazional(db_trimestre_sazional=db_trimestre_sazional)

    data1 = ts.colum_taxa_var(taxas1=taxas1)

    data1 = ts.formatando_data(taxas1=taxas1)

    data1 = ts.col_trimestre1(data1=data1)

    # Save 
    ssd.save_csv(
        df= data1,
        path= config_silver['data1']['save_path'])

    if show_plots:
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
    print('----- EMPREGO -----')
    # Taxa de desocupação 
    # Read 
    db_taxa_desemprego = rd.read_csv(config_raw['db_taxa_desemprego']['path'])

    # Transform
    db_taxa_desemprego = ts.transf_tx_desemprego(db_taxa_desemprego=db_taxa_desemprego)

    # Save 
    ssd.save_csv(
        df= db_taxa_desemprego,
        path= config_silver['db_taxa_desemprego']['save_path'])

    #Plot
    if show_plots:
        fig = px.line(db_taxa_desemprego, y=db_taxa_desemprego['Valor'], x=db_taxa_desemprego['Trimestre Móvel'])
        fig.show()

    #Tipos de emprego 
    # Read 
    db_tipos_emprego = rd.read_csv(config_raw['db_tipos_emprego']['path'])

    # Transform 
    var_percent_tipo_emprego = ts.trans_tipos_emprego(db_tipos_emprego=db_tipos_emprego)

    # Save 
    ssd.save_csv(
        df= var_percent_tipo_emprego,
        path= config_silver['var_percent_tipo_emprego']['save_path'])

    # Plot
    if show_plots:
        fig = px.line(var_percent_tipo_emprego, x='Trimestre Móvel', y='Valor', color='Posição na ocupação e categoria do emprego no trabalho principal',
                    title='Gráfico de Linhas por Categoria de Emprego')
        fig.update_layout(xaxis_title='Trimestre Móvel', yaxis_title='Valor')

        fig.show()

    # Transform - - Pivot 
    pivot_var_percent_tipo_empreg = ts.transf_var_percent_tipo_emprego(var_percent_tipo_emprego=var_percent_tipo_emprego)

    # Save 
    ssd.save_csv(
        df= pivot_var_percent_tipo_empreg,
        path= config_silver['pivot_var_percent_tipo_empreg']['save_path'])

    #Grandes Regiões 
    # Read 
    db_grandes_regioes = rd.read_csv(config_raw['db_grandes_regioes']['path'])

    # Transform 
    db_grandes_regioes = ts.transf_db_grandes_regioes(db_grandes_regioes=db_grandes_regioes)

    # Save 
    ssd.save_csv(
        df= db_grandes_regioes,
        path= config_silver['db_grandes_regioes']['save_path'])

    # Plot
    if show_plots:
        fig = px.line(db_grandes_regioes, x='Trimestre', y='Valor', color='Grande Região',
                    title='Taxa de desocupacao das pessoas com 14 anos o mais de idade, na semana de referencia (em %) - Grandes regioes ')
        fig.update_layout(xaxis_title='Trimestre', yaxis_title='Valor')
        fig.show()

    # Sexo 
    # Read
    db_desempre_sexo = rd.read_csv(config_raw['db_desempre_sexo']['path'])

    # Transform
    db_desempre_sexo = ts.transf_db_desempre_sexo(db_desempre_sexo=db_desempre_sexo)

    # Save 
    ssd.save_csv(
        df= db_desempre_sexo,
        path= config_silver['db_desempre_sexo']['save_path'])

    # Plot 
    if show_plots:
        fig = px.line(db_desempre_sexo, x='Trimestre', y='Valor', color='Sexo',
                    title='Taxa de desocupacao das pessoas de 14 anos ou mais, na semana de refernecia, por sexo (%)')
        fig.update_layout(xaxis_title='Trimestre', yaxis_title='Valor')
        fig.show()

    # Transformacoes da diferenca entre homens e mulheres 
    merge_homem_mulher = ts.trans_diferenca(db_desempre_sexo=db_desempre_sexo)

    # Save
    ssd.save_csv(
        df= merge_homem_mulher,
        path= config_silver['merge_homem_mulher']['save_path'])

    # Plot
    if show_plots:
        fig = px.line(db_desempre_sexo, x='Trimestre', y='Valor', color='Sexo',
                    title='Taxa de desocupacao das pessoas de 14 anos ou mais, na semana de refernecia, por sexo (%)')
        fig.update_layout(xaxis_title='Trimestre', yaxis_title='Valor')
        fig.update_layout(yaxis2=dict(title='', overlaying='y', side='right'))
        fig.add_scatter(x=merge_homem_mulher['Trimestre'], y=merge_homem_mulher['diferenca'], 
                        fill='tozeroy', mode='lines', name='Diferença percentual entre homens e mulheres', yaxis='y2')
        fig.show()    
        
        
    # Por idade 
    #Read
    db_pop_idade = rd.read_csv(config_raw['db_pop_idade']['path'])

    # Transform 
    db_pop_idade = ts.transf_por_idade(db_pop_idade=db_pop_idade)

    # Save
    ssd.save_csv(
        df= db_pop_idade,
        path= config_silver['db_pop_idade']['save_path'])

    # Plot
    if show_plots:
        fig = px.line(db_pop_idade, x='Trimestre', y='Valor', color='Grupo de idade',
                    title='Taxa de desocupação, por idade, 1º trimestre 2012 - 2º trimestre 2023')

        fig.update_layout(xaxis_title='Trimestre', yaxis_title='Valor')
        fig.show()

    # Rendimento regiao  
    # Read
    rendimento_regiao = rd.read_csv(config_raw['rendimento_regiao']['path'])
    rendimento_regiao_br = rd.read_csv(config_raw['rendimento_regiao_br']['path']) 

    # Transform 
    rendimento_regiao_1 = ts.transf_rendimento_regiao(rendimento_regiao_br=rendimento_regiao_br, rendimento_regiao=rendimento_regiao)

    # Save
    ssd.save_csv(
        df= rendimento_regiao_1,
        path= config_silver['rendimento_regiao_1']['save_path'])

    # Plot
    if show_plots:
        fig = px.line(rendimento_regiao_1, x='Trimestre', y='Valor', color='Grandes Regiões',
                    title='Rendimento Médio, por grande região, 1º trimestre 2012 - 2º trimestre 2023')
        fig.update_layout(xaxis_title='Trimestre', yaxis_title='Valor')
        fig.show()

    # Rendimento por idade 
    # Transform 
    rendimento_idade = ts.transf_rendimento_idade(rendimento_regiao_br=rendimento_regiao_br)

    # Save 
    ssd.save_csv(
        df= rendimento_regiao_br,
        path= config_silver['rendimento_regiao_br']['save_path'])

    ssd.save_csv(
        df= rendimento_idade,
        path= config_silver['rendimento_idade']['save_path'])

    # Plot
    if show_plots:
        fig = px.line(rendimento_idade, x='Trimestre', y='Valor', color='Grupo de idade',
                    title='Rendimento Médio, por idade, 1º trimestre 2012 - 2º trimestre 2023')
        fig.update_layout(xaxis_title='Trimestre', yaxis_title='Valor')
        fig.show()

    # Dados Caged
    # Read
    dados_admissoes = rd.read_csv(config_raw['dados_admissoes']['path'])
    dados_demissoes = rd.read_csv(config_raw['dados_demissoes']['path'])
    dados_saldo = rd.read_csv(config_raw['dados_saldo']['path'])

    #Transform 
    dados_caged = ts.transf_dados_caged(dados_admissoes=dados_admissoes, dados_demissoes=dados_demissoes, dados_saldo=dados_saldo)

    # Save
    ssd.save_csv(
        df= dados_caged,
        path= config_silver['dados_caged']['save_path'])


    #Plot
    if show_plots:
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
    print('----- CRÉDITO -----')
    #Read
    dados_credito = rd.read_csv(config_raw['dados_credito']['path'])
    ipca_credito = rd.read_csv(config_raw['ipca_credito']['path'])
    

    #Transform 
    dados_credito = ts.tratamento_dados_credito(dados_credito= dados_credito)
    ipca_credito = ts.tratamento_ipca_credito(ipca_credito=ipca_credito)

    
    concessoes = ts.deflacionando_dessazonalizando(dados_credito=dados_credito, ipca_credito=ipca_credito)

    # Save 
    ssd.save_csv(
        df= dados_credito,
        path= config_silver['dados_credito']['save_path'])

    ssd.save_csv(
        df= ipca_credito,
        path= config_silver['ipca_credito']['save_path'])

    ssd.save_csv(
        df= concessoes,
        path= config_silver['concessoes']['save_path'])
    
    # IPCA 15 
    print('----- IPCA 15 -----')
    #Calc IPCA 15
    # Read
    ipca_15 = rd.read_csv(config_silver['ipca_15']['read_path'])
    # Transform
    ipca_15_mensal = ts.ipca_15_mensal(ipca_15)
    ipca_15_acum12m = ts.ipca_15_acum12m(ipca_15)
    # Save
    ssd.save_csv(
    df=ipca_15_mensal, 
    path=config_silver['ipca_15_mensal']['save_path']
    )
    
    ssd.save_csv(
    df=ipca_15_acum12m, 
    path=config_silver['ipca_15_acum12m']['save_path']
    )
    
    
if __name__ == '__main__':
    run_silver(
        config_silver=config_silver,
        config_raw=config_raw,
        )