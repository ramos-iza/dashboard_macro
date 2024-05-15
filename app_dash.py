import plotly.graph_objects as go 
import config 
import gold_data.read_data as rd
import silver_data.save_silver_data as ssd
import silver_data.transform_silver as ts
import plotly.graph_objects as go 
import plotly.express as px
import matplotlib
import config 
import streamlit as st
from datetime import date
import pandas as pd 
from plotly.subplots import make_subplots

# Grupos IPCA
df_geral_ipca = rd.read_csv(config.silver['df_geral_ipca']['save_path'])
indice_geral = rd.read_csv(config.silver['indice_geral']['save_path'])

grupos_ipca = (df_geral_ipca.set_index('data')).columns

#IPCA mensal x IPCA acum 12m
juntos = rd.read_csv(config.silver['juntos']['save_path'])

# ultima data - ipca acumulado 
dados_brutos_ipca_sidra = rd.read_csv(config.raw['dados_brutos_ipca_sidra']['path'])
ultima_data = ts.last_date(dados_brutos_ipca_sidra=dados_brutos_ipca_sidra)

#IPCA ao ano por região metropolitana
ipca_rm = rd.read_csv(config.silver['ipca_rm']['save_path'])

#Comparar a médias dos núcleos com o IPCA histórico
nucleo_ipca_merge = rd.read_csv(config.silver['nucleo_ipca_merge']['save_path'])

#Silver IPCA núcleo
nucleo_long= rd.read_csv(config.silver['nucleo_long']['save_path'])
ipca_nucleo = rd.read_csv(config.raw['ipca_nucleo']['path'])

#PIB ajuste sazonal 
data1 = rd.read_csv(config.silver['data1']['save_path'])

#PIB 
data = rd.read_csv(config.silver['data']['save_path'])

# EMPREGO
#Caged
dados_caged = rd.read_csv(config.silver['dados_caged']['save_path'])

# Taxa de desemprego
db_taxa_desemprego = rd.read_csv(config.silver['db_taxa_desemprego']['save_path'])

# Por tipo de emprego 
var_percent_tipo_emprego = rd.read_csv(config.silver['var_percent_tipo_emprego']['save_path'])

pivot_var_percent_tipo_empreg = rd.read_csv(config.silver['pivot_var_percent_tipo_empreg']['save_path'])

# Grandes regioes 
db_grandes_regioes = rd.read_csv(config.silver['db_grandes_regioes']['save_path'])

# Por faixa de idade 
db_pop_idade = rd.read_csv(config.silver['db_pop_idade']['save_path'])

# Por sexo
db_desempre_sexo = rd.read_csv(config.silver['db_desempre_sexo']['save_path'])
merge_homem_mulher = rd.read_csv(config.silver['merge_homem_mulher']['save_path'])

# Rendimento região
rendimento_regiao_1 = rd.read_csv(config.silver['rendimento_regiao_1']['save_path'])

# Rendimento por idade 
rendimento_idade = rd.read_csv(config.silver['rendimento_idade']['save_path'])

# Para o primeiro gráfico - IPCA mensal e acumulado 
ipca_mes = rd.read_csv(config.silver['ipca_mes']['save_path'])
ipca_acum_12m = rd.read_csv(config.silver['ipca_acum_12m']['save_path'])
ipca_acum_12m['data'] = pd.to_datetime(ipca_acum_12m['data'])

# Crédito 
dados_credito = rd.read_csv(config.silver['dados_credito']['save_path'])
ipca_credito = rd.read_csv(config.silver['ipca_credito']['save_path'])
concessoes = rd.read_csv(config.silver['concessoes']['save_path'])

# IPCA 15 
ipca_15_mensal = rd.read_csv(config.silver['ipca_15_mensal']['save_path'])
ipca_15_acum12m = rd.read_csv(config.silver['ipca_15_acum12m']['save_path'])

container_cs = """
<style>
    .main {
        padding: 0;
    }
</style>
"""

st.set_page_config(layout="wide")

# Aplica o CSS personalizado ao Streamlit
st.markdown(container_cs, unsafe_allow_html=True)


with st.sidebar.expander("Dash macro", expanded=False):
    pass

aba = st.sidebar.radio('Escolha a aba', ['IPCA', 'PIB', 'EMPREGO', 'CRÉDITO'])

if aba == 'IPCA': 
    
    def ipca():
        
        col1, col2 = st.columns(2)
        with col1:
            #st.write(f"<h1 style='text-align: center;'>{''}</h1>", unsafe_allow_html=True) # para não escrever nada
            hoje = date.today().strftime('%d/%m/%Y')
            st.markdown(f"<h1 style='color: #171616; font-size: 38px; text-align: left;'>{'IPCA'}</h1>", unsafe_allow_html=True)#(f"<h1 style='text-align: center;'>{'IPCA'}</h1>", unsafe_allow_html=True)
            st.markdown (f"<h6 style='color: #eb4c34; font-size: 17px; text-align: left;'>{hoje}</h6>", unsafe_allow_html=True) # ou data da análise f"<h2 style='text-align: center;'>{'IPCA'}</h1>", unsafe_allow_html=True
            #st.subheader('xxxx')
            
    ipca()  
    
    col1, col2, col3 = st.columns(3)
    with col1:   
        st.image('imagem7.jpeg')

        
    with col2: 
        st.image('imagem10.jpeg')
        
    with col3: 
        st.image('imagem9.jpeg')

    with st.expander('IPCA - Mensal e Acumulado em 12 meses', expanded=True):    
        fig = go.Figure()
        fig.add_trace(go.Bar(x= ipca_mes['data'], y =ipca_mes['V'], name = 'IPCA mensal', marker=dict(color='#f06e35')))
        fig.add_trace(go.Bar(x=ipca_acum_12m['data'], y=ipca_acum_12m['ipca_acum_ano'], name = 'IPCA acumulado 12 m', marker=dict(color='#6980EA')))
        fig.update_layout(height=535,title={'text': f'IPCA - Mensal e Acumulado nos ultimos 12 meses', 'font': {'size': 16}})
        st.plotly_chart(fig, use_container_width=True, responsive=True)
            

    col1, col2 = st.columns(2)
    with col1: 
        with st.expander('IPCA grupos', expanded=True):
            col3, col4 = st.columns(2)
            with col3:
                df_geral_ipca = df_geral_ipca.set_index('data')
                opcoes = df_geral_ipca.columns.tolist()
                opcoes_selecao = st.selectbox('Selecione os grupos do IPCA', opcoes)    
                     
            dados_filtrados = df_geral_ipca[opcoes_selecao]
            fig = go.Figure()
            indice_geral_data = indice_geral.reset_index()
            fig.add_trace(go.Scatter(x=indice_geral['data'], y=indice_geral['valor'], name='Índice Geral', marker=dict(color='#6980EA')))
            fig.add_trace(go.Scatter(x=indice_geral['data'], y=dados_filtrados.values, name='Grupo', line=dict(color='#f06e35')))
            st.plotly_chart(fig, use_container_width=True, responsive=True)
           
    with col2: 
        with st.expander('IPCA mensal x IPCA acum 12m', expanded = True):
            
 
            fig = go.Figure()
            fig.add_trace(go.Bar(x = juntos['valor_y'], y = juntos['grupo'], name = 'Variação acumulada ao ano', orientation='h',  marker=dict(color='#6980EA')))
            fig.add_trace(go.Bar(x = juntos['valor_x'], y = juntos['grupo'], name = 'Variação mensal',  orientation='h', marker=dict(color='#f06e35')))
            fig.update_layout(height=535,title={'text': f'IPCA - Variação mensal e acumulada no ano (%) - Índice geral e grupos de produtos e serviços - Brasil - {ultima_data}', 'font': {'size': 11.89}})
            fig.update_yaxes(categoryorder='category descending')
            st.plotly_chart(fig, use_container_width=True, responsive=True)
            
    with st.expander('IPCA 15 - Mensal e Acumulado em 12 meses', expanded=True):   
        fig = go.Figure()
        fig.add_trace(go.Bar(x= ipca_15_mensal['D2N'], y =ipca_15_mensal['V'], name = 'IPCA 15 mensal', marker=dict(color='#f06e35')))
        fig.add_trace(go.Bar(x=ipca_15_acum12m['D2N'], y=ipca_15_acum12m['V'], name = 'IPCA 15 acumulado 12 m', marker=dict(color='#6980EA')))
        fig.update_layout(height=535,title={'text': f'IPCA 15 - Mensal e Acumulado nos últimos 12 meses', 'font': {'size': 16}})
        st.plotly_chart(fig, use_container_width=True, responsive=True) 
                
            
    with st.expander('IPCA região metropolitana', expanded=True):
            
            paleta_cores_candy = ['#FF80B3', '#FFE08C', '#FFA680', '#AED9CC', '#FFD39B', '#8080FF', '#D580D5', '#C3A0C3', '#A9A9A9', '#FFB3B3']
            fig = px.bar(ipca_rm, x='ano', y='valor', color='Região Metropolitana', barmode='group', color_discrete_sequence=paleta_cores_candy)
            fig.update_layout(title_text = 'IPCA - Variação acumulada no ano', xaxis={'type':'category'})
            st.plotly_chart(fig, use_container_width=True, responsive=True) 
            
    
    col1, col2 = st.columns(2)     
    with col1:    
        with st.expander('Média dos Núcleos x IPCA', expanded = True):
        
            check = st.checkbox('Quer saber o que são os núcleos?')    
            if check == True: 
                            st.write('Os núcleos do IPCA são subíndices que buscam analisar a variação de preços de uma cesta de produtos e serviços excluindo itens que podem ter variações atípicas ou temporárias, a fim de obter uma medida mais estável e confiável da inflação. Eles são usados para ajudar a compreender melhor as tendências de inflação de longo prazo, filtrando ruídos causados por choques temporários nos preços de certos produtos.')
                    
            fig = go.Figure()
            fig.add_trace(go.Scatter(x= nucleo_ipca_merge['Date'], y= nucleo_ipca_merge['media'], name='Média dos núcleos', line=dict(color='#6980EA')))
            fig.add_trace(go.Scatter(x= nucleo_ipca_merge['Date'], y= nucleo_ipca_merge['ipca_anual'], name='IPCA Anual', line=dict(color='#f06e35'))) #6980EA
            fig.update_layout(title_text='Média dos núcleos x IPCA')
            st.plotly_chart(fig, use_container_width=True, responsive=True)    
            
    with col2:    
        with st.expander('IPCA Núcleo', expanded = True):
            
            paleta_cores_candy = ['#FF80B3', '#FFE08C', '#FFA680', '#AED9CC', '#FFD39B', '#8080FF', '#A9A9A9', '#FFB3B3']
            fig = px.bar(nucleo_long, x='Date', y= 'valor', color='Núcleos', barmode='group', color_discrete_sequence=paleta_cores_candy)
            fig.update_layout(height=490, title_text = 'Núcleos do IPCA', xaxis={'type' : 'category'})
            st.plotly_chart(fig, use_container_width=True, responsive=True)     

# PIB            
            
if aba == 'PIB': 
    
    def pib():
        
        col1, col2 = st.columns(2)
        with col1:
            #st.write(f"<h1 style='text-align: center;'>{''}</h1>", unsafe_allow_html=True) # para não escrever nada
            hoje = date.today().strftime('%d/%m/%Y')
            st.markdown(f"<h1 style='color: #171616; font-size: 38px; text-align: left;'>{'PIB'}</h1>", unsafe_allow_html=True)#(f"<h1 style='text-align: center;'>{'IPCA'}</h1>", unsafe_allow_html=True)
            st.markdown (f"<h6 style='color: #eb4c34; font-size: 17px; text-align: left;'>{hoje}</h6>", unsafe_allow_html=True) # ou data da análise f"<h2 style='text-align: center;'>{'IPCA'}</h1>", unsafe_allow_html=True
            #st.subheader('xxxx')
            
    pib()  
    
    col1, col2, col3 = st.columns(3)
    with col1:   
        st.image('imagem7.jpeg')

        
    with col2: 
        st.image('imagem10.jpeg')
        
    with col3: 
        st.image('imagem9.jpeg')
        
    # pib ajuste sazonal
    with st.expander('', expanded = True):
    

        check = st.checkbox('Quer saber mais sobre a variação trimestral do PIB?')    
        if check == True: 
            st.write('É o crescimento do PIB em comparação ao trimestre anterior, na série com ajuste sazonal.\n\n' 
                        'O ajuste sazonal do PIB trimestral é uma forma de limpar os efeitos das mudanças sazonais, como feriados ou estações do ano, dos dados econômicos para que possamos entender melhor como a economia está realmente se saindo. Isso nos ajuda a ver as tendências reais e nos permite comparar os trimestres de maneira justa. Basicamente, é como tirar o "ruído" dos dados para que possamos ver a imagem econômica mais clara.\n\n'
                        'Origem dos Dados: Dados extraídos da API SIDRA.')
        
        fig = go.Figure()
        fig.add_trace(go.Bar(x=data1['trimestre'], y=data1['Var. % margem'], name='xxxx', marker=dict(color='#6980EA')))
        fig.update_layout(title= 'PIB: Série Encadeada do Índice de Volume Trimestral com ajuste sazonal', title_font=dict(size=19), xaxis=dict(tickangle=45))
        st.plotly_chart(fig, use_container_width=True, responsive=True)
    
    # pib variação interanual
    with st.expander('', expanded = True):

        check = st.checkbox('Quer saber mais sobre a taxa de variação interanual do PIB?')    
        if check == True: 
            st.write('A variação do PIB interanual se refere à diferença percentual do PIB, em relação ao mesmo trimestre ou período do ano anterior. Em outras palavras, ela nos permite avaliar como a economia está se saindo em comparação com o mesmo período do ano anterior.\n\n'
                     'Obs.: sem ajuste sazonal.\n\n'
                        'Origem dos Dados: Dados extraídos da API SIDRA.')
        
        
        fig = go.Figure()
        fig.add_trace(go.Bar(x=data['trimestre'], y=data['Var. % interanual'], name='xxxx', marker_color='#f06e35'))
        fig.update_layout(title = 'PIB: Taxas de Variação Interanual', title_font=dict(size=19), xaxis=dict(tickangle=45))
        st.plotly_chart(fig, use_container_width=True, responsive=True)
        
    
     
    # pib variacao anual     
    with st.expander('', expanded = True):
        
        check = st.checkbox('Quer mais sobre a taxa de acumulada?')    
        if check == True: 
            st.write('Acumulamos a taxa a em quatro trimestres e comparamos com o mesmo período anterior. Exemplo: o PIB acumulado nos quatro trimestres terminados em junho de 2023 cresceu 3,2% em relação aos quatro trimestres imediatamente anteriores. \n\n'
                     'Obs.: sem ajuste sazonal.\n\n'
                     'Origem dos Dados: Dados extraídos da API SIDRA.')
        
        
        fig = go.Figure()
        fig.add_trace(go.Bar(x=data['trimestre'], y=data['Var. % anual'], name='xxxx',  marker=dict(color='#6980EA')))
        fig.update_layout(title = 'PIB: Taxa Acumulado em Quatro Trimestres', title_font=dict(size=19), xaxis=dict(tickangle=45))
        st.plotly_chart(fig, use_container_width=True, responsive=True)
        
    # pib acumulado no ano 
    with st.expander('', expanded = True):

        check = st.checkbox('Quer mais sobre a acumulada do PIB?')    
        if check == True: 
            st.write('O PIB acumulado no ano em relação ao mesmo período do ano anterior.\n\n'
                     'Obs.: sem ajuste sazonal.\n\n'
                     'Origem dos Dados: Dados extraídos da API SIDRA.')
        
        fig = go.Figure()
        fig.add_trace(go.Bar(x=data['trimestre'], y=data['Var. % acumulada no ano'], name='xxxx', marker_color='#f06e35'))
        fig.update_layout(title = 'PIB: Taxa de variação acumulada no ano', title_font=dict(size=19), xaxis=dict(tickangle=45))
        st.plotly_chart(fig, use_container_width=True, responsive=True)
        
        
# Emprego           
            
if aba == 'EMPREGO': 
    
    def emprego():
        
        col1, col2 = st.columns(2)
        with col1:
            #st.write(f"<h1 style='text-align: center;'>{''}</h1>", unsafe_allow_html=True) # para não escrever nada
            hoje = date.today().strftime('%d/%m/%Y')
            st.markdown(f"<h1 style='color: #171616; font-size: 38px; text-align: left;'>{'Emprego'}</h1>", unsafe_allow_html=True)#(f"<h1 style='text-align: center;'>{'IPCA'}</h1>", unsafe_allow_html=True)
            st.markdown (f"<h6 style='color: #eb4c34; font-size: 17px; text-align: left;'>{hoje}</h6>", unsafe_allow_html=True) # ou data da análise f"<h2 style='text-align: center;'>{'IPCA'}</h1>", unsafe_allow_html=True
            #st.subheader('xxxx')
            
    emprego()  
    
    col1, col2, col3 = st.columns(3)
    with col1:   
        st.image('imagem7.jpeg')

        
    with col2: 
        st.image('imagem10.jpeg')
        
    with col3: 
        st.image('imagem9.jpeg')
        
    # dados caged 
    with st.expander('', expanded = True):
    
        check = st.checkbox('Selecione a caixa de seleção para saber mais informações sobre o CAGED')    
        if check == True: 
            st.write('Série com ajuste sazonal.\n'
                     '\n O Novo Caged (Cadastro Geral de Empregados e Desempregados) é um sistema de registro e acompanhamento do mercado de trabalho no Brasil. Tem como objetivo principal acompanhar as movimentações de empregados e desempregados no país, fornecendo informações essenciais sobre o mercado de trabalho. \n'
                     '\n Empregadores são obrigados a fornecer informações detalhadas sobre seus funcionários, incluindo nome, CPF, data de admissão, data de demissão (se aplicável), cargo, remuneração, entre outros.')
        
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
            title='Evolução das Admissões, Demissões e Saldo no Novo CAGED',
            xaxis=dict(title='Período'),
            yaxis=dict(title='Admissões e Demissões'),
            yaxis2=dict(
                title='Saldo',
                overlaying='y',
                side='right',
                title_font=dict(size=19)
            ),
            plot_bgcolor='white'  # Defina o fundo como branco
        )
        # Crie a figura com os objetos Bar e Scatter e o layout
        fig = go.Figure(data=[bar_admissoes, bar_demissoes, scatter_saldo], layout=layout)
        st.plotly_chart(fig, use_container_width=True, responsive=True)
        
        
    # Taxa de desemprego - PNAD
    with st.expander('', expanded = True):

        check = st.checkbox('Selecione a caixa de seleção para saber mais informações sobre o PNAD')    
        if check == True: 
            st.write('PNAD é a abreviação de Pesquisa Nacional por Amostra de Domicílios, um levantamento que costuma ser conduzido pelo IBGE para coletar informações demográficas e socioeconômicas em residências selecionadas por meio de amostragem.\n'
                     '\n É um estudo que classifica a população em dois grupos principais:'
                     '\n\n **1. Maiores de 14 anos aptos a trabalhar:** Isso inclui pessoas com idade suficiente para trabalhar, ou seja, aquelas com 14 anos ou mais.'
                     '\n\n **2. Menores de 14 anos considerados não aptos:** Isso abrange as pessoas com menos de 14 anos, que geralmente não são consideradas aptas para o trabalho.'
                     '\n\n Dentro do grupo de pessoas com idade para trabalhar, existem duas categorias adicionais:'
                     '\n\n **1. Pessoas na força de trabalho:** Isso engloba aquelas que estão atualmente trabalhando ou procurando ativamente por emprego.'
                     '\n\n **2. Pessoas fora da força de trabalho:** São aquelas que não estão trabalhando e também não estão buscando emprego ativamente. Isso pode incluir estudantes em tempo integral, aposentados, donas de casa que não estão procurando emprego, entre outros.'
                     '\n\n Portanto, ao calcular a taxa de desemprego, não consideramos as pessoas que estão fora da força de trabalho, ou seja, aquelas que não estão trabalhando e também não estão buscando ativamente emprego. A taxa de desemprego é calculada dividindo o número de desocupados pelo total de pessoas na força de trabalho, que inclui apenas aqueles que estão procurando emprego.'
                    )
        
        fig = px.line(db_taxa_desemprego, y=db_taxa_desemprego['Valor'], x=db_taxa_desemprego['Trimestre Móvel'])
        fig.update_layout(title='Taxa de Desocupação - PNAD',title_font=dict(size=17), xaxis=dict(tickangle=45))
        fig.update_traces(line=dict(color='#6980EA'))  
        st.plotly_chart(fig, use_container_width=True, responsive=True)
   
    # Por grandes regiões 
    col1, col2 = st.columns(2)     
    with col1:    
        with st.expander('', expanded = True):
            
            paleta_cores_candy = ['#FF80B3', '#8080FF', '#A9A9A9', '#AED9CC', '#FFD39B']     
            fig = px.line(db_grandes_regioes, x='Trimestre', y='Valor', color='Grande Região',
                        title='Taxa de desocupacao das pessoas com 14 anos o mais de idade, PNAD - Grandes regioes', color_discrete_sequence=paleta_cores_candy)
            fig.update_layout(height=490, xaxis_title='Trimestre', yaxis_title='Valor', title_font=dict(size=15.5))
            st.plotly_chart(fig, use_container_width=True, responsive=True)  
    
    # Por faixa de idade        
    with col2:    
        with st.expander('', expanded = True):

            paleta_cores_candy = ['#FF80B3', '#A9A9A9', '#FFA680', '#AED9CC', '#FFD39B', '#8080FF']
            fig = px.line(db_pop_idade, x='Trimestre', y='Valor', color='Grupo de idade',
                        title='Taxa de desocupacao das pessoas com 14 anos o mais de idade, PNAD - Por idade', color_discrete_sequence=paleta_cores_candy)

            fig.update_layout(xaxis_title='Trimestre', yaxis_title='Valor', title_font=dict(size=15.5))
            st.plotly_chart(fig, use_container_width=True, responsive=True)    
            
    # Por sexo 
    with st.expander('', expanded = True):

        paleta_cores_candy = ['#8080FF', '#A9A9A9', '#FFA680']
        fig = px.line(db_desempre_sexo, x='Trimestre', y='Valor', color='Sexo',
                    title='Taxa de desocupacao das pessoas com 14 anos o mais de idade, PNAD - Por sexo', color_discrete_sequence=paleta_cores_candy)
        fig.update_layout(xaxis_title='Trimestre', yaxis_title='Valor')
        fig.update_layout(yaxis2=dict(title='', overlaying='y', side='right'), title_font=dict(size=17), xaxis=dict(tickangle=45))
        fig.add_scatter(x=merge_homem_mulher['Trimestre'], y=merge_homem_mulher['diferenca'], 
                        fill='tozeroy', mode='lines', name='Diferença percentual entre homens e mulheres', yaxis='y2', fillcolor='rgba(0, 0, 255, 0.09)',  line=dict(color='rgba(0, 0, 255, 0.09)'))
        st.plotly_chart(fig, use_container_width=True, responsive=True)               
            
    # Rendimento por idade, por região    
    col1, col2 = st.columns(2)     
    with col1:    
        with st.expander('', expanded = True):
        
            paleta_cores_candy = ['#FF80B3', '#A9A9A9', '#FFA680', '#AED9CC', '#FFD39B', '#8080FF']                    
            fig = px.line(rendimento_regiao_1, x='Trimestre', y='Valor', color='Grandes Regiões',
                        title='Rendimento Médio, PNAD - Grandes Regiões', color_discrete_sequence=paleta_cores_candy)
            fig.update_layout(height=452.5, xaxis_title='Trimestre', yaxis_title='Valor')
            st.plotly_chart(fig, use_container_width=True, responsive=True)
    
    # Por faixa de idade        
    with col2:    
        with st.expander('', expanded = True):

            paleta_cores_candy = ['#FF80B3', '#A9A9A9', '#FFA680', '#AED9CC', '#FFD39B', '#8080FF'] 
            fig = px.line(rendimento_idade, x='Trimestre', y='Valor', color='Grupo de idade',
                title='Rendimento Médio, PNAD - Por idade', color_discrete_sequence=paleta_cores_candy)
            fig.update_layout(xaxis_title='Trimestre', yaxis_title='Valor')
            st.plotly_chart(fig, use_container_width=True, responsive=True)

               
    # Por tipo de emprego 
    with st.expander('', expanded=True):
    

        geral =pivot_var_percent_tipo_empreg.set_index(['Trimestre Móvel', 'Trimestre Móvel (Código)'])
        opcoes1 = pivot_var_percent_tipo_empreg.columns.tolist()
        if 'Trimestre Móvel (Código)' in opcoes1:
            opcoes1.remove('Trimestre Móvel (Código)')
        if 'Trimestre Móvel' in opcoes1:
            opcoes1.remove('Trimestre Móvel')
        if 'Total' in opcoes1:
            opcoes1.remove('Total')
        opcoes_selecao1 = st.selectbox('Selecione o tipo de emprego', opcoes1)    
        
             
        dados_filtrados1 = pivot_var_percent_tipo_empreg[[opcoes_selecao1, 'Trimestre Móvel']]
        

        fig = go.Figure()
        total = var_percent_tipo_emprego[var_percent_tipo_emprego['Posição na ocupação e categoria do emprego no trabalho principal'] == 'Total'].set_index('Trimestre Móvel')
        fig.add_trace(go.Scatter(x=total.index, y=total['Valor'], name='Total', line=dict(color='#6980EA'))) #marker=dict(color='#6980EA')
        fig.add_trace(go.Scatter(x=dados_filtrados1['Trimestre Móvel'], y=dados_filtrados1[opcoes_selecao1], name='Tipo de emprego', line=dict(color='#f06e35')))
        fig.update_layout(title='Taxa de Desocupação - PNAD', xaxis_title='Trimestre', yaxis_title='Valor', title_font=dict(size=17), xaxis=dict(tickangle=45))
        st.plotly_chart(fig, use_container_width=True, responsive=True)
    
if aba == 'CRÉDITO': 
    
    def credito():
        
        col1, col2 = st.columns(2)
        with col1:
            #st.write(f"<h1 style='text-align: center;'>{''}</h1>", unsafe_allow_html=True) # para não escrever nada
            hoje = date.today().strftime('%d/%m/%Y')
            st.markdown(f"<h1 style='color: #171616; font-size: 38px; text-align: left;'>{'CRÉDITO'}</h1>", unsafe_allow_html=True)#(f"<h1 style='text-align: center;'>{'IPCA'}</h1>", unsafe_allow_html=True)
            st.markdown (f"<h6 style='color: #eb4c34; font-size: 17px; text-align: left;'>{hoje}</h6>", unsafe_allow_html=True) # ou data da análise f"<h2 style='text-align: center;'>{'IPCA'}</h1>", unsafe_allow_html=True
            #st.subheader('xxxx')
            
    credito()  
    
    col1, col2, col3 = st.columns(3)
    with col1:   
        st.image('imagem7.jpeg')

        
    with col2: 
        st.image('imagem10.jpeg')
        
    with col3: 
        st.image('imagem9.jpeg')

    # Concessão de crédito 
    col1, col2 = st.columns(2)     
    with col1:    
        with st.expander('', expanded = True):
                           
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=dados_credito['data'], y=dados_credito["Concessões de crédito - Total"] / 1000, mode='lines', line=dict(color='#6980EA')))
            fig.update_layout(title='Concessões de crédito - Total\n Valores nominais.<br>Dados: BCB', yaxis_title="R$ bilhões", title_font=dict(size=15.5), height=490)
            st.plotly_chart(fig, use_container_width=True, responsive=True)
    
    # Concessão de crédito deflacionada e com ajuste sazional         
    with col2:    
        with st.expander('', expanded = True):

            check = st.checkbox('Selecione a caixa de seleção para saber mais sobre o ajuste sazional')    
            if check == True: 
                st.write('Dados ajustado sazonalmente pelo X13-SEATS-ARIMA.\n'
                        '\n O X13-SEATS-ARIMA incorpora técnicas avançadas de análise de séries temporais, incluindo a modelagem ARIMA (Médias Móveis Integradas Autoregressivas), bem como a capacidade de lidar com efeitos sazonais e de calendário, como feriados e dias úteis.'
                        '\n .')            

            data_atual = concessoes['data'] = pd.to_datetime(concessoes['data'])
            data_atual = concessoes.tail(1)["data"].dt.strftime("%b/%Y").item()
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=concessoes["data"], y=concessoes["ajuste"], mode='lines', line=dict(color='#f06e35')))
            fig.update_layout(title=f"Concessões de crédito - Total<br>Valores deflacionados pelo IPCA a preços de {data_atual} e com ajuste sazonal.<br>Dados: BCB/IBGE", #ajustado sazonalmente pelo X13-SEATS-ARIMA.
                            yaxis_title="R$ bilhões", title_font=dict(size=15.5))
            st.plotly_chart(fig, use_container_width=True, responsive=True)
            
            
    #Concessões de crédito - público/privado, livre/direcionado
    with st.expander('', expanded=True):
            
        fig = make_subplots(rows=2, cols=2)
        fig.add_trace(go.Scatter(x=dados_credito['data'], y=dados_credito["Concessões de crédito - PF"] / 1000, mode='lines', name='Concessões de crédito - PF', line=dict(color='#FFD39B')), row=1, col=1)
        fig.add_trace(go.Scatter(x=dados_credito['data'], y=dados_credito["Concessões de crédito - PJ"] / 1000, mode='lines', name='Concessões de crédito - PJ', line=dict(color='#A9A9A9')), row=1, col=2)
        fig.add_trace(go.Scatter(x=dados_credito['data'], y=dados_credito["Concessões de crédito - Livre"] / 1000, mode='lines', name='Concessões de crédito - Livre', line=dict(color='#FFA680')), row=2, col=1)
        fig.add_trace(go.Scatter(x=dados_credito['data'], y=dados_credito["Concessões de crédito - Direcionado"] / 1000, mode='lines', name='Concessões de crédito - Direcionado', line=dict(color='#AED9CC')), row=2, col=2)
        fig.update_layout(
            title='Concessões de crédito <br>Valores nominais<br>Dados: BCB',
            yaxis_title="R$ bilhões",
            width=1000,  # Largura total do gráfico
            height=600,   # Altura total do gráfico
        )
        st.plotly_chart(fig, use_container_width=True, responsive=True)
        
    # Concessão de crédito - PF x PJ 
    col1, col2 = st.columns(2)     
    with col1:
        with st.expander('', expanded = True):
            
            
            x = dados_credito['data']
            y_pf = dados_credito["Concessões de crédito - PF"] / dados_credito["Concessões de crédito - Total"] * 100
            y_pj = dados_credito["Concessões de crédito - PJ"] / dados_credito["Concessões de crédito - Total"] * 100
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=x, y=y_pf, fill='tozeroy', mode='none', name='PF', stackgroup='stack'))
            fig.add_trace(go.Scatter(x=x, y=y_pj, fill='tozeroy', mode='none', name='PJ', stackgroup='stack'))
            fig.update_layout(title=f"Concessão de crédito Pessoa Física x Pessoa Jurídica<br>Dados: BCB",
                            yaxis_title="% Total", 
                            legend_title="Categorias")
            st.plotly_chart(fig, use_container_width=True, responsive=True)
    
    # Concessão de crédito - livre x direcionado         
    with col2:    
        with st.expander('', expanded = True):      
            
            x = dados_credito['data']
            y_livre = dados_credito["Concessões de crédito - Livre"] / dados_credito["Concessões de crédito - Total"] * 100
            y_direcionada = dados_credito["Concessões de crédito - Direcionado"] / dados_credito["Concessões de crédito - Total"] * 100
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=x, y=y_livre, fill='tozeroy', mode='none', name='Livre', stackgroup='stack'))
            fig.add_trace(go.Scatter(x=x, y=y_direcionada, fill='tozeroy', mode='none', name='Direcionado', stackgroup='stack'))
            fig.update_layout(title=f"Concessão de crédito Livre x Direcionada<br>Dados: BCB",
                            yaxis_title="% Total", 
                            legend_title="Categorias")
            st.plotly_chart(fig, use_container_width=True, responsive=True)
        
    # Estoque 
    col1, col2 = st.columns(2)     
    with col1:
        with st.expander('', expanded = True):
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=dados_credito["data"], y=dados_credito["Saldo da carteira de crédito - Total"] / dados_credito["PIB acumulado dos últimos 12 meses"] * 100, fill='tozeroy', mode='none'))
            fig.update_layout(title=f"Estoque de Crédito<br>Dados: BCB", 
                            yaxis_title="R$ bilhões",height=490)
            st.plotly_chart(fig, use_container_width=True, responsive=True)
        
    # Estoque - Privado/Publico % do Total   
    with col2:    
        with st.expander('', expanded = True):
            
            dados_credito = dados_credito.set_index('data')
            x = dados_credito.index
            y_privado = dados_credito["Saldos de crédito - Privado"] / dados_credito["Saldo da carteira de crédito - Total"] * 100
            y_publico = dados_credito["Saldos de crédito - Público"] / dados_credito["Saldo da carteira de crédito - Total"] * 100
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=x, y=y_privado, fill='tozeroy', mode='none', name='Privado', stackgroup='stack'))
            fig.add_trace(go.Scatter(x=x, y=y_publico, fill='tozeroy', mode='none', name='Público', stackgroup='stack'))
            fig.update_layout(title=f"Estoque de Crédito<br>Dados: BCB",
                            yaxis_title="% Total", 
                            legend_title="Categorias")
            st.plotly_chart(fig, use_container_width=True, responsive=True)
            
    
    #Taxa de juros - mercado de crédito 
    col1, col2 = st.columns(2)     
    with col1:    
        with st.expander('', expanded = True):
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=dados_credito.index, y=dados_credito["Taxa média de juros das operações de crédito"], mode='lines', line=dict(color='#FFA680')))
            fig.update_layout(title=f"Taxa Média de Juros das Novas Concessões de Crédito - Mercado de Crédito - Brasil<br>Dados: BCB", 
                            yaxis_title="% a.a.", height=490)
            st.plotly_chart(fig, use_container_width=True, responsive=True)
    
    # Spread bancário        
    with col2:    
        with st.expander('', expanded = True):
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=dados_credito.index, y=dados_credito["Spread médio das operações de crédito"], mode='lines', line=dict(color='#AED9CC')))
            fig.update_layout(title=f"Spread Bancário - Mercado de Crédito - Brasil<br>Dados: BCB", 
                            yaxis_title="p.p.", height=490)
            st.plotly_chart(fig, use_container_width=True, responsive=True)
            
    # Inadimplência 
    with st.expander('', expanded = True):
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dados_credito.index, y=dados_credito["Inadimplência da carteira de crédito"], mode='lines', line=dict(color='#FFB3B3')))
        fig.update_layout(title=f"Inadimplência - Mercado de Crédito - Brasil<br>Dados: BCB", 
                        yaxis_title="p.p.")
        st.plotly_chart(fig, use_container_width=True, responsive=True)
    

        
    

        