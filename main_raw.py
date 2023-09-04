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
