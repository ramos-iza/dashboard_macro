
import pandas as pd

def ipca_mensal(ipca_mensal, path): 
   ipca_mensal.to_csv(path)
   
      
def dados_brutos_ipca_sidra(dados_brutos_ipca_sidra, path):
    dados_brutos_ipca_sidra.to_csv(path)

    
def ipca_focus(ipca_focus, path):
   ipca_focus.to_csv(path)
   
   
def ipca_rm (ipca_rm, path):
   ipca_rm.to_csv(path) 
   

def ipca_nucleo(ipca_nucleo, path): 
   ipca_nucleo.to_csv(path)   
   
# Pib 
def pib_volume_trimestral(pib_volume_trimestral, path):
   pib_volume_trimestral.to_csv(path)  
   

def db_trimestre_sazional(db_trimestre_sazional, path):
   db_trimestre_sazional.to_csv(path)

   
def db_taxa_desemprego(db_taxa_desemprego, path):
   db_taxa_desemprego.to_csv(path) 
   
   
def db_tipos_emprego(db_tipos_emprego, path):
   db_tipos_emprego.to_csv(path) 
   
   
def db_grandes_regioes(db_grandes_regioes, path):
   db_grandes_regioes.to_csv(path) 
   
def db_desempre_sexo(db_desempre_sexo, path):
   db_desempre_sexo.to_csv(path) 
   
   
def db_pop_idade(db_pop_idade, path):
   db_pop_idade.to_csv(path) 
   
   
def rendimento_regiao(rendimento_regiao, path):
   rendimento_regiao.to_csv(path) 
   
   
def rendimento_regiao_br(rendimento_regiao_br, path):
   rendimento_regiao_br.to_csv(path) 
   
   
def dados_admissoes(dados_admissoes, path):
   dados_admissoes.to_csv(path) 
   
def dados_demissoes(dados_demissoes, path):
   dados_demissoes.to_csv(path) 

def dados_saldo(dados_saldo, path):
   dados_saldo.to_csv(path) 

def dados_credito(dados_credito, path):
   dados_credito.to_csv(path) 
   
def ipca_credito(ipca_credito, path):
   ipca_credito.to_csv(path) 
   
def save_to_csv(df, path):
   df.to_csv(path) 