from config import raw as config
#import modulo1
import raw_data.get_raw_data as grd
import raw_data.save_raw_data as srd


ipca_mensal = grd.ipca_mensal(
    start_date=config['ipca_mensal']['start_date']
)

srd.ipca_mensal(
    ipca_mensal=ipca_mensal, 
    path=config['ipca_mensal']['path']
)

dados_brutos_ipca_sidra = grd.dados_brutos_ipca_sidra()

srd.dados_brutos_ipca_sidra(
    dados_brutos_ipca_sidra=dados_brutos_ipca_sidra,
    path=config['dados_brutos_ipca_sidra']['path']
    )

ipca_focus = grd.ipca_focus()

srd.ipca_focus(
    ipca_focus=ipca_focus, 
    path=config['ipca_focus']['path']
    )


ipca_rm = grd.ipca_rm()

srd.ipca_rm(ipca_rm=ipca_rm, 
            path=config['ipca_rm']['path'])


ipca_nucleo = grd.ipca_nucleo()

srd.ipca_nucleo(ipca_nucleo=ipca_nucleo,
                path=config['ipca_nucleo']['path'])


# Pib 

pib_volume_trimestral = grd.pib_volume_trimestral()

srd.pib_volume_trimestral(pib_volume_trimestral=pib_volume_trimestral,
                path=config['pib_volume_trimestral']['path'])


db_trimestre_sazional = grd.db_trimestre_sazional()

srd.db_trimestre_sazional(db_trimestre_sazional=db_trimestre_sazional,
                path=config['db_trimestre_sazional']['path'])

# Emprego 

db_taxa_desemprego = grd.db_taxa_desemprego()

srd.db_taxa_desemprego(db_taxa_desemprego=db_taxa_desemprego,
                path=config['db_taxa_desemprego']['path'])


db_tipos_emprego = grd.db_tipos_emprego()

srd.db_tipos_emprego(db_tipos_emprego=db_tipos_emprego,
                path=config['db_tipos_emprego']['path'])


db_grandes_regioes = grd.db_grandes_regioes()

srd.db_grandes_regioes(db_grandes_regioes=db_grandes_regioes,
                path=config['db_grandes_regioes']['path'])


db_desempre_sexo = grd.db_desempre_sexo()

srd.db_desempre_sexo(db_desempre_sexo=db_desempre_sexo,
                path=config['db_desempre_sexo']['path'])


db_pop_idade = grd.db_pop_idade()

srd.db_pop_idade(db_pop_idade=db_pop_idade,
                path=config['db_pop_idade']['path'])


rendimento_regiao = grd.rendimento_regiao()

srd.rendimento_regiao(rendimento_regiao=rendimento_regiao,
                path=config['rendimento_regiao']['path'])


rendimento_regiao_br = grd.rendimento_regiao_br()

srd.rendimento_regiao_br(rendimento_regiao_br=rendimento_regiao_br,
                path=config['rendimento_regiao_br']['path'])


dados_admissoes = grd.dados_admissoes()

srd.dados_admissoes(dados_admissoes=dados_admissoes,
                path=config['dados_admissoes']['path'])

dados_demissoes = grd.dados_demissoes()

srd.dados_demissoes(dados_demissoes=dados_demissoes,
                path=config['dados_demissoes']['path'])


dados_saldo = grd.dados_saldo()

srd.dados_saldo(dados_saldo=dados_saldo,
                path=config['dados_saldo']['path'])