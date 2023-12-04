from config import raw as config_raw
from main_raw import run_raw

from config import silver as config_silver
from main_silver import run_silver

from main_gold import run_gold


if __name__ == '__main__':

    print('--- Running Raw ---')
    run_raw(config=config_raw)
 
    print('--- Running Silver ---')
    run_silver(
        config_silver=config_silver,
        config_raw=config_raw,   
    )
    
    
    print('---Running_gold---')
    run_gold(
        config_silver=config_silver,
        config_raw=config_raw,   
    )