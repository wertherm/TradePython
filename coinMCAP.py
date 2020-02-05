import json
import coinmarketcap
from decimal import Decimal

def CoinMarketCap():
    market = coinmarketcap.Market()
    coin = market.ticker("bitcoin") #Retorna o tipo 'list'
    
    #Para fazer a formatação de casas decimais, primeiro é necessário converter de string para decimal.
    #O índice '0' é o único que contém dados ou seja todos os itens do json em um tipo 'list'
    mcap = Decimal(coin[0]['market_cap_usd'])
    vol24 = Decimal(coin[0]['24h_volume_usd'])
    
    print('Market Cap: {0:,}'.format(mcap))
    print('Volume em 24H: {0:,}'.format(vol24))
