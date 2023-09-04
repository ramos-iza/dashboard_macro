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


#Grupos IPCA 
def trat_grupo_ipca(dados_brutos_ipca_sidra):
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
    return ipca_analise          

def cal_df_geral_ipca(ipca_analise):
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
            comunicacao = comunicacao.groupby(comunicacao['data'].dt.strftime('%Y-%m')).mean()['valor'].to_frame().rename(columns={'valor':'Comunicação'})
    df_geral_ipca = pd.concat([alimentacao_bebidas, habitacao, artigos_residencia, vestuario, transportes, saude, despesas_pessoais, educacao, comunicacao], axis =1)
    df_geral_ipca.columns = ['Alimentação e bebidas', 'Habitação', 'Artigos de residência', 'Vestuário', 'Transportes', 'Saúde', 'Despesas Pessoais', 'Educação', 'Comunicação']    
    return df_geral_ipca


def indice_geral(ipca_analise):
    indice_geral = ipca_analise.query('grupo == "Índice geral"')
    indice_geral = indice_geral.groupby(indice_geral['data'].dt.strftime('%Y-%m')).mean()['valor'].to_frame()
    return indice_geral

'''def calc_proporcao(df_geral_ipca): 
    df_geral_ipca_data = df_geral_ipca
    proporcao = df_geral_ipca_data.iloc[-2,:].to_frame()
    proporcao['total'] = proporcao.values.sum().T
    proporcao['proporcao'] = proporcao['2023-03']/proporcao['total']
    return proporcao'''

'''Gold
    labels = pd.to_datetime(['Alimentação e bebidas',	'Habitação', 'Artigos de residência', 'Vestuario','Transportes',	'Saúde', 'Despesas pessoais', 'Educação',	'Comunicação'])
    values = pd.to_datetime([0.014803,	0.091779,	0.034541,	0.048850,	0.164018,	0.177144,	0.167909,	0.150622,	0.150334])
    return labels, values'''
    
#IPCA ao ano por região metropolitana
def trasform_ipca_rm(ipca_rm):
    ipca_rm = ipca_rm.filter(items= ['V', 'D1N', 'D2C', 'D3N']).rename(columns = {
        'V': 'valor', 'D1N' : 'Região Metropolitana', 'D2C' : 'data', 'D3N' : 'Variável'}).iloc[1:].assign(
            data = lambda x: pd.to_datetime(x.data, format = '%Y%m')).assign(valor = lambda y: y.valor.astype(float))
    ipca_rm['mes'] = ipca_rm['data'].dt.month 
    ipca_rm = ipca_rm.query('mes == 12')   
    ipca_rm['ano'] = ipca_rm['data'].dt.year
    return ipca_rm       


#Silver IPCA núcleo
def calc_nucleos_ipca(ipca_nucleo):
    nucleos_analise = ipca_nucleo#.reset_index()
    nucleos_analise['Date'] = pd.to_datetime(nucleos_analise['Date'])
    nucleos_analise['ano'] = nucleos_analise.Date.dt.year
    nucleos_maior_21 = nucleos_analise.query('ano >= 2019').set_index('Date')
    nucleos_maior_21 = nucleos_maior_21.apply(lambda x: (x / 100 + 1)).reset_index()
    nucleos_maior_21 = nucleos_maior_21.groupby(nucleos_maior_21['Date'].dt.year).prod()
    nucleos_maior_21 = nucleos_maior_21.apply(lambda x: (x - 1) * 100).iloc[:,:8]

    nucleo_long  = nucleos_maior_21.reset_index()
    nucleo_long = pd.melt(nucleo_long, id_vars = ['Date'], value_vars = ['IPCA-EX0', 'IPCA-EX1', 'IPCA-EX2', 'IPCA-EX3', 'IPCA-MA', 'IPCA-MS', 'IPCA-DP', 'IPCA-P55'], var_name = 'Núcleos', value_name = 'valor')
    return nucleo_long

#Comparar a médias dos núcleos com o IPCA histórico
def calc_comp_media_nucleos(ipca_nucleo, ipca_anual):
    ipca_nucleo_ano = ipca_nucleo.set_index('Date').apply(lambda x: (x / 100 + 1)).reset_index().dropna()
    ipca_nucleo_ano = ipca_nucleo_ano.groupby(ipca_nucleo_ano['Date'].dt.year).prod()
    ipca_nucleo_ano = ipca_nucleo_ano.drop('ano', axis=1)
    ipca_nucleo_ano['media'] = ipca_nucleo_ano.mean(axis=1)
    ipca_nucleo_ano = ipca_nucleo_ano.query('Date >= 2013 and Date < 2023')
    ipca_nucleo_ano = ipca_nucleo_ano.apply(lambda x: ipca_nucleo_ano['media'] - 1)
    ipca_anual1 = ipca_anual.query('Date >= 2013 and Date < 2023').set_index('Date')
    nucleo_ipca_merge = pd.concat([ipca_nucleo_ano, ipca_anual1], axis=1)
    return nucleo_ipca_merge


#IPCA mensal x IPCA acum 12m
def calc_p_nova_analise(dados_brutos_ipca_sidra): 
    ipca_analise_novo = (dados_brutos_ipca_sidra.rename(columns= dados_brutos_ipca_sidra.iloc[0]).query('Valor not in "Valor"').rename(columns = {
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
    return ipca_analise_novo


def calc_valor_mensal(ipca_analise_novo):
    vm_grupos = ipca_analise_novo.query('variavel == "IPCA peso mensal"').set_index('data').rename(columns={'valor':'vm_grupos'})
    return vm_grupos


def calc_ipca_acum_ano(ipca_analise_novo):
    ipca_acum_ano = ipca_analise_novo.query('variavel	== "IPCA % acum. ano"').set_index('data').rename(columns={'valor':'ipca_acum_ano'})
    return ipca_acum_ano
 
def juntando_tab(vm_grupos):
    todas_listas = []
    vm_grupos = vm_grupos.reset_index()
    for numero in range(1, 10):
        numero_str = str(numero) + '.'
        linhas_com_n = vm_grupos.loc[vm_grupos['grupo'].str.startswith(numero_str)]
        lista = linhas_com_n.values.tolist()
        todas_listas.append(lista)
        tabela = pd.concat([pd.DataFrame(lista) for lista in todas_listas], ignore_index=True).rename(columns = {0: 'data', 1:'variavel', 2:'grupo', 3:'valor'})
    return tabela

'''
def geral_ipca():
    geral_ipca = pd.concat([alimentacao_bebidas, habitacao, artigos_residencia, vestuario, transportes, saude, despesas_pessoais, educacao, comunicacao], axis =1)'''

def calc_acum_corrente(ipca_acum_ano, tabela):
    ipca_acum_ano = ipca_acum_ano.reset_index()
    todas_listas = []
    for numero in range(1, 10):
        numero_str = str(numero) + '.'
        linhas_com_n = ipca_acum_ano.loc[ipca_acum_ano['grupo'].str.startswith(numero_str)]
        lista = linhas_com_n.values.tolist()
        todas_listas.append(lista)
        tabela_acum = pd.concat([pd.DataFrame(lista) for lista in todas_listas], ignore_index=True).rename(columns = {0: 'data', 1:'variavel', 2:'grupo', 3:'valor'})
    ultima_data = (tabela.data.iloc[-1]).date()
    data_formatada = ultima_data.strftime('%Y-%m-%d')   
    tabela_acum_mes_corrente = tabela_acum[tabela_acum['data'] == data_formatada]
    return tabela_acum_mes_corrente

def trat_peso_mensal_corrente(tabela):
    ultima_data = (tabela.data.iloc[-1]).date()
    data_formatada = ultima_data.strftime('%Y-%m-%d')
    peso_mensal_corrente = tabela[tabela['data'] == data_formatada]
    return peso_mensal_corrente

def juntando_ipca_corrente(peso_mensal_corrente, tabela_acum_mes_corrente):
    juntos = peso_mensal_corrente.merge(tabela_acum_mes_corrente, on = ['grupo', 'data'])[['data', 'grupo', 'variavel_x', 'valor_x', 'variavel_y', 'valor_y']] 
    return juntos 
    
def last_date(dados_brutos_ipca_sidra):
    ultima_data = dados_brutos_ipca_sidra.D2N.iloc[-1]
    return ultima_data
    
# PIB

def calc_dados_margem(pib_volume_trimestral):
    db_trimestre = pib_volume_trimestral
    dados_margem = db_trimestre.rename(columns = db_trimestre.iloc[0]).query("Trimestre not in 'Trimestre'").rename(columns={
                "Trimestre (Código)": "data",
                "Setores e subsetores": "rubrica",
                "Valor": "valor",
                "Unidade de Medida" : "tabela"
                }).filter(items = ["tabela", "data", "rubrica", "valor"], axis = "columns").replace(to_replace = {
                "rubrica": {
                    "Agropecuária - total": "Agropecuária",
                    "Indústria - total": "Indústria",
                    "Serviços - total": "Serviços",
                    "PIB a preços de mercado": "PIB",
                    "Despesa de consumo das famílias": "Consumo das Famílias",
                    "Despesa de consumo da administração pública": "Despesa do Governo",
                    "Formação bruta de capital fixo": "FBFC",
                    "Exportação de bens e serviços": "Exportação",
                    "Importação de bens e serviços (-)": "Importação"
                    }
                    }
                ).replace(to_replace = {
                "tabela": {
                    "Número-índice": "num_indice"}})
                
    dados_margem = dados_margem.assign(  # substitui o 5º caracter da coluna data por "-Q" e converte em YYYY-MM-DD
    data = lambda x: pd.to_datetime(
        x.data.str.slice_replace(start = 4, stop = 5, repl = "-Q")
        ),
    valor = lambda x: x.valor.astype(float) # converte de texto para numérico
        )
    
    dados_margem['mes'] = dados_margem['data'].dt.month
    dados_margem['ano'] =  dados_margem['data'].dt.year
    
    return dados_margem



def define_trimestre(row): 
    if row['mes'] in range(1,4):
        return str(row['ano']) + '.I'
    elif row['mes'] in range(4,7):
        return str(row['ano']) + '.II'
    elif row['mes'] in range(7,10):
        return str(row['ano']) + '.III'
    elif row['mes'] in range(10,13):
        return str(row['ano']) + '.IV'
    else:
        return ''
    
def col_trimestre(dados_margem):
    dados_margem['trimestre'] = dados_margem.apply(define_trimestre, axis=1)

    return dados_margem


def calc_taxa_var(dados_margem):
    taxas = (
    dados_margem.query("tabela in ['num_indice', 'num_indice_sa']")
    .pivot(index = ["data", "rubrica"], columns = "tabela", values = "valor")
    .reset_index()
    .sort_values("data")
    )
    
    taxas["trimestre"] = dados_margem["trimestre"]
     
    return taxas

def calc_variacao_interanual(taxas):
    taxas["ano"] = taxas["data"].dt.year
    # variação interanual
    taxas["var_interanual"] = (
    taxas.groupby("rubrica")["num_indice"]
    .apply(lambda x: x.pct_change(4) * 100))
    
    # variação anual 
    taxas["var_anual"] = (
    taxas.groupby("rubrica")["num_indice"] # soma móvel de 4 períodos
    .apply(lambda x: (x.rolling(4).sum() / x.rolling(4).sum().shift(4) - 1) * 100))
    
    #indice acumulado 
    taxas["num_indice_acum"] = (
    taxas.groupby(["rubrica", "ano"])["num_indice"]
    .apply(lambda x: x.cumsum()) # acumula o número índice por ano/rubrica
    )
    taxas["var_acum_ano"] = (
    taxas.groupby("rubrica")["num_indice_acum"]
    .apply(lambda x: x.pct_change(4) * 100))

    return taxas

def filtrando_pib(taxas):
    data = (
    taxas.query("rubrica == 'PIB'")
    .rename(
        columns={
            "var_interanual": "Var. % interanual",
            "var_anual": "Var. % anual",
            "var_acum_ano": "Var. % acumulada no ano"
            }))
    return data

# Pib sazional 
def calc_pib_tri_sazional(db_trimestre_sazional):
    db_trimestre_sazional = db_trimestre_sazional.rename(columns = db_trimestre_sazional.iloc[0]).query("Trimestre not in 'Trimestre'").rename(columns={
                "Trimestre (Código)": "data",
                "Setores e subsetores": "rubrica",
                "Valor": "valor",
                "Unidade de Medida" : "tabela"
                }).filter(items = ["tabela", "data", "rubrica", "valor"], axis = "columns").replace(to_replace = {
                "rubrica": {
                    "Agropecuária - total": "Agropecuária",
                    "Indústria - total": "Indústria",
                    "Serviços - total": "Serviços",
                    "PIB a preços de mercado": "PIB",
                    "Despesa de consumo das famílias": "Consumo das Famílias",
                    "Despesa de consumo da administração pública": "Despesa do Governo",
                    "Formação bruta de capital fixo": "FBFC",
                    "Exportação de bens e serviços": "Exportação",
                    "Importação de bens e serviços (-)": "Importação"
                    }
                    }
                ).replace(to_replace = {
                "tabela": {
                    "Número-índice": "num_indice_sa"}})

    db_trimestre_sazional = db_trimestre_sazional.assign(  # substitui o 5º caracter da coluna data por "-Q" e converte em YYYY-MM-DD
    data = lambda x: pd.to_datetime(
        x.data.str.slice_replace(start = 4, stop = 5, repl = "-Q")
        ),
    valor = lambda x: x.valor.astype(float) # converte de texto para numérico
        )
    
    db_trimestre_sazional['mes'] = db_trimestre_sazional['data'].dt.month
    db_trimestre_sazional['ano'] =  db_trimestre_sazional['data'].dt.year
    
    return db_trimestre_sazional


def calc_taxa_var_sazional(db_trimestre_sazional):
    taxas1 = (
    db_trimestre_sazional.query("tabela in ['num_indice_sa']")
    .pivot(index = ["data", "rubrica"], columns = "tabela", values = "valor")
    .reset_index()
    .sort_values("data")
    )
    return taxas1

def colum_taxa_var(taxas1):
    taxas1["var_margem"] = (
    taxas1.groupby("rubrica")["num_indice_sa"] # agrupa os dados e aponta a coluna
    .apply(lambda x: x.pct_change(1) * 100))   # calcula a variação na coluna
    
    taxas1["ano"] = taxas1["data"].dt.year
    taxas1['mes'] = taxas1['data'].dt.month
    return taxas1
    
    
def formatando_data(taxas1):    
    data1 = (
    taxas1.query("rubrica == 'PIB'")
    .rename(
        columns={"var_margem": "Var. % margem",
            }))
    return data1


def define_trimestre(row): 
    if row['mes'] in range(1,4):
        return str(row['ano']) + '.I'
    elif row['mes'] in range(4,7):
        return str(row['ano']) + '.II'
    elif row['mes'] in range(7,10):
        return str(row['ano']) + '.III'
    elif row['mes'] in range(10,13):
        return str(row['ano']) + '.IV'
    else:
        return ''
    
def col_trimestre1(data1):
    data1['trimestre'] = data1.apply(define_trimestre, axis=1)
    return data1


