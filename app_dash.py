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

aba = st.sidebar.radio('Escolha a aba', ['IPCA', 'PIB'])

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
            fig.add_trace(go.Scatter(x=indice_geral['data'], y=indice_geral['valor'], name='Índice Geral', line=dict(color='blue')))
            fig.add_trace(go.Scatter(x=indice_geral['data'], y=dados_filtrados.values, name='Grupo', line=dict(color='#f06e35')))
            st.plotly_chart(fig, use_container_width=True, responsive=True)
           
    with col2: 
        with st.expander('IPCA mensal x IPCA acum 12m', expanded = True):
            
 
            fig = go.Figure()
            fig.add_trace(go.Bar(x = juntos['valor_y'], y = juntos['grupo'], name = 'Variação acumulada ao ano', orientation='h'))
            fig.add_trace(go.Bar(x = juntos['valor_x'], y = juntos['grupo'], name = 'Variação mensal',  orientation='h', marker=dict(color='#f06e35')))
            fig.update_layout(height=535,title={'text': f'IPCA - Variação mensal e acumulada no ano (%) - Índice geral e grupos de produtos e serviços - Brasil - {ultima_data}', 'font': {'size': 12}})
            fig.update_yaxes(categoryorder='category descending')
            st.plotly_chart(fig, use_container_width=True, responsive=True)
            
            
            
    with st.expander('IPCA região metropolitana', expanded=True):
            
            
            fig = px.bar(ipca_rm, x='ano', y='valor', color='Região Metropolitana', barmode='group')
            fig.update_layout(title_text = 'IPCA - Variação acumulada no ano', xaxis={'type':'category'})
            st.plotly_chart(fig, use_container_width=True, responsive=True) 
            
    
    col1, col2 = st.columns(2)     
    with col1:    
        with st.expander('Média dos Núcleos x IPCA', expanded = True):
        
            check = st.checkbox('Quer saber o que são os núcleos?')    
            if check == True: 
                            st.write('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed maximus, turpis vitae consectetur consectetur, mauris felis volutpat urna, vel dictum est quam ac magna. Nulla consequat facilisis sapien, eget tristique risus facilisis eu. Suspendisse suscipit sem id eros tincidunt, in rhoncus ligula lacinia.')
                    
            fig = go.Figure()
            fig.add_trace(go.Scatter(x= nucleo_ipca_merge['Date'], y= nucleo_ipca_merge['media'], name='Média dos núcleos'))
            fig.add_trace(go.Scatter(x= nucleo_ipca_merge['Date'], y= nucleo_ipca_merge['ipca_anual'], name='IPCA Anual', line=dict(color='#f06e35')))
            fig.update_layout(title_text='Média dos núcleos x IPCA')
            st.plotly_chart(fig, use_container_width=True, responsive=True)    
            
    with col2:    
        with st.expander('IPCA Núcleo', expanded = True):

            fig = px.bar(nucleo_long, x='Date', y= 'valor', color='Núcleos', barmode='group')
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
        fig.add_trace(go.Bar(x=data1['trimestre'], y=data1['Var. % margem'], name='xxxx'))
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
        fig.add_trace(go.Bar(x=data['trimestre'], y=data['Var. % anual'], name='xxxx'))
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
        
        







                  
            
