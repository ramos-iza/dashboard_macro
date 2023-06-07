import plotly.graph_objects as go 
import config 
import gold_data.read_data as rd
import silver_data.save_silver_data as ssd
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

#IPCA ao ano por região metropolitana
ipca_rm = rd.read_csv(config.silver['ipca_rm']['save_path'])

#Comparar a médias dos núcleos com o IPCA histórico
nucleo_ipca_merge = rd.read_csv(config.silver['nucleo_ipca_merge']['save_path'])

#Silver IPCA núcleo
nucleo_long= rd.read_csv(config.silver['nucleo_long']['save_path'])
ipca_nucleo = rd.read_csv(config.raw['ipca_nucleo']['path'])



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

aba = st.sidebar.radio('Escolha a aba', ['IPCA'])

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
            
            with col4:     
                min_index = 0
                max_index = len(indice_geral) 
                selected_index = st.slider('Selecione o período', min_value=min_index, max_value=max_index, value=(min_index, max_index))
                
                start_index, end_index = selected_index
                x_values = indice_geral['data'].iloc[start_index:end_index+1]
                     
            dados_filtrados = df_geral_ipca[opcoes_selecao]
            fig = go.Figure()
            indice_geral_data = indice_geral.reset_index()
            fig.add_trace(go.Scatter(x=x_values, y=indice_geral['valor'], name='Índice Geral', line=dict(color='blue')))
            fig.add_trace(go.Scatter(x=x_values, y=dados_filtrados.values, name='Grupo', line=dict(color='#f34a00')))
            fig.update_layout(width=610, height=400)
            st.plotly_chart(fig)
            
    with col2: 
        with st.expander('IPCA mensal x IPCA acum 12m', expanded = True):

            fig = go.Figure()
            fig.add_trace(go.Bar(x = juntos['valor_y'], y = juntos['grupo'], name = 'Variação acumulada ao ano', orientation='h'))
            fig.add_trace(go.Bar(x = juntos['valor_x'], y = juntos['grupo'], name = 'Variação mensal',  orientation='h', marker=dict(color='#f34a00')))
            fig.update_layout(title={'text': 'IPCA - Variação mensal e acumulada no ano (%) - Índice geral e grupos de produtos e serviços - Brasil - abril 2023', 'font': {'size': 12}})
            fig.update_layout(width=610, height=500)
            fig.update_yaxes(categoryorder='category descending')
            st.plotly_chart(fig)
            
            
            
    with st.expander('IPCA região metropolitana', expanded=True):
            
            
            fig = px.bar(ipca_rm, x='ano', y='valor', color='Região Metropolitana', barmode='group')
            fig.update_layout(title_text = 'IPCA - Variação acumulada no ano', xaxis={'type':'category'})
            fig.update_layout(width=1200, height=400)
            st.plotly_chart(fig) 
            
    
    col1, col2 = st.columns(2)     
    with col1:    
        with st.expander('Média dos Núcleos x IPCA', expanded = True):
        
            check = st.checkbox('Quer saber o que são os núcleos?')    
            if check == True: 
                            st.write('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed maximus, turpis vitae consectetur consectetur, mauris felis volutpat urna, vel dictum est quam ac magna. Nulla consequat facilisis sapien, eget tristique risus facilisis eu. Suspendisse suscipit sem id eros tincidunt, in rhoncus ligula lacinia.')
                    
            fig = go.Figure()
            fig.add_trace(go.Scatter(x= nucleo_ipca_merge['Date'], y= nucleo_ipca_merge['media'], name='Média dos núcleos'))
            fig.add_trace(go.Scatter(x= nucleo_ipca_merge['Date'], y= nucleo_ipca_merge['ipca_anual'], name='IPCA Anual', line=dict(color='#f34a00')))
            fig.update_layout(title_text='Média dos núcleos x IPCA')
            fig.update_layout(width=610, height=400)
            st.plotly_chart(fig)    
            
    with col2:    
        with st.expander('IPCA Núcleo', expanded = True):

            fig = px.bar(nucleo_long, x='Date', y= 'valor', color='Núcleos', barmode='group')
            fig.update_layout(title_text = 'Núcleos do IPCA', xaxis={'type' : 'category'})
            fig.update_layout(width=610, height=441)
            st.plotly_chart(fig)     
           
               





                  
            
