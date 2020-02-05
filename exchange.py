#Parse Json
#----------
#No Python o parse Json é realizado pela library 'import json'. Existem duas funções nesta biblioteca, json.dumps e json.loads, e no python existem dois tipos de estrutura para manipular (Handler) o json 'str' e 'dict'.
#O json.dumps serve para 'descarregar' um objeto Json do tipo 'dict' (Dictionary) ou 'list' para ser consumido externamente à aplicação, convertendo-o para o tipo 'str' (String).
#O json.loads serve para consumir um response json do tipo 'str' e convertê-lo em um 'dict', assim permitindo que a estrutura Json possa ser indexada como um array, dentro do python. Você poderá manipular o json usando por exemplo: print(jsonDict['campo')

#--dataDict = bittrex.fetch_ticker('BTC/USDT') #Função que já retorna o response Json como um tipo Dictionary, assim não necessitando usar o json.loads()

#Exemplo de Python to Json - Pega o Response Json do tipo dictionary e cria um objeto Json do tipo String Identada, para ser consumida fora da aplicação.
#   dataStr = json.dumps(bittrex.fetch_ticker('BTC/USDT'), indent=2)
#Exemplo de Json to Python - Pega o objeto Json do tipo string e cria um Dictionary Tipado, pois od valores do array são convertidos automaticamente em string, float, integer etc.
#   dataDict = json.loads(dataStr)

#--print(dataDict['ask'])

import ccxt #Você pode usar este módulo só para parsear os response json públicos, mas na hora que precisar executar métodos privados das exchanges, onde é necessário passar a secret, você pode criar um algoritimo próprio sem utilizar o módulo CCXT.
import json

#print(ccxt.exchanges)
#print(mercadobitcoin.loadMarkets())

#Exemplo Parse To An Object
class objJson(object):
    def __init__(self, data):
        self.__dict__ = json.loads(data)

def BuscarCotacao(nomeExchange, par):
    try:
        #Fica um pouco redundante converter um dictionary em uma string para passá-la para a classe objJson que a converte novamente em dictionary. Mas é só para exemplificar como fazer o parse do json dentro de uma classe, onde o parâmetro 'object' precisa ser uma string.
        if nomeExchange == 'BitTrex':
            exchange = ccxt.bittrex()
        elif nomeExchange == 'MercadoBitcoin':
            exchange = ccxt.mercado()
        
        exchangeRetorno = objJson(json.dumps(exchange.fetch_ticker(par)))
        cotacao = exchangeRetorno.ask
    except ccxt.DDoSProtection as e:
        print(type(e).__name__, e.args, 'DDoS Protection (ignoring)')
    except ccxt.RequestTimeout as e:
        print(type(e).__name__, e.args, 'Request Timeout (ignoring)')
    except ccxt.ExchangeNotAvailable as e:
        print(type(e).__name__, e.args, 'Exchange Not Available due to downtime or maintenance (ignoring)')

    return cotacao

def BuscarOHLCV(nomeExchange, par, timeFrame, limite):
    if nomeExchange == 'BitTrex':
        exchange = ccxt.bittrex()
    elif nomeExchange == 'MercadoBitcoin':
        exchange = ccxt.mercado()

    #Serve para ver se a exchange possui dados de OHLCV ou se é emulado, como no caso do Mercado Bitcoin.
    #print(exchange.has['fetchOHLCV'])

    return exchange.fetch_ohlcv(par, timeFrame, limit=limite)

    """
    exchange.timeframes: #Será vazio se !has.fetchOHLCV
        '1m': '1minute',
        '1h': '1hour',
        '1d': '1day',
        '1M': '1month',
        '1y': '1year',
    """
