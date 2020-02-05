#Estratégias
#O algoritimo ping-pong possui uma estratégia semelhante à estratégia da RSI. Pois as operações de compra e venda são executadas dentro de uma faixa de intervalo do preço de compra ou venda. No caso do ping-pong, esta faixa é sempre fixa, o que é ruim quando o preço sobe ou desce demais, ficando assim a faixa muito longe do objetivo de compra e venda.
#O algoritimo da RSI já possui uma estratégia um pouco mais dinâmica, a faixa de intervalo do preço de compra ou venda, se altera dinâmicamente em relação à uma média dos preços de abertura e fechamento.
#Já o algoritimo da Bollinger Band é melhor para criar uma faixa dinâmica mais curta do que a RSI, assim as operações são executadas mais rapidamente, pois as ordens de outros traders, são programadas assim que o preço encosta nas bandas.

#Estatisticas
#O algoritimo fica comprando e vendendo (Ping-Pong) assim que atinge a variação de valorExtrapolado, para cima ou para baixo. Para detectar um 'pump' ou 'dump' ele fica analizando o aumento ou diminuição dessa variação, caso ultrapasse 40% para cima ou para baixo, o algoritimo ping-pong irá parar. Apartir daí o robo não fica mais aguardando atingir a variação e compra ou vende na mesma hora, alterando valorCompraInicial.
#Antes de comprar ou vender, você pode analisar se a tendência é de queda ou subida. Pois se você comprar em uma tendência de queda, é provável que o robo ficará um bom tempo sem vender.

import time
from termcolor import colored

import exchange

#Constantes
valorCompra = 8000 #Este é o preço inicial para comprar
valorVenda = 0
margemOperacao = 20 #Se extrapolar $20 da cotação da compra ou da venda, executa a operação
cotacaoDolarReal = 3.4
spreadMinimo = 50

def RetornarCotacao(nomeExchange, par):
    cotacao = exchange.BuscarCotacao(nomeExchange, par)
    
    if nomeExchange == 'MercadoBitcoin':
        cotacao = cotacao / cotacaoDolarReal

    return cotacao

#Se o spread é maior no Brasil, transfere dos EUA para o Brasil e vende. A partir daí, fica executando somente o ping-pong no Brasil, ao mesmo tempo que aguarda o preço ficar mais baixo nos EUA em relação ao spread ganho na primeira operação para transferir e recomprar nos EUA, assim reiniciando o ciclo.
def CalcularSpread(cotacao, cotacaoEUA):
    spread = cotacao - cotacaoEUA
    
    if spread >= spreadMinimo:
        print(colored('Cotação no Brasil é maior que nos EUA, com spread de: ${} '.format(spread), 'blue'))
    elif spread < 0: #Spread Negativo, ocorre quando a cotação dos EUA é maior do que no Brasil.
        print(colored('Cotação no EUA é maior que no Brasil, com spread de: ${} '.format(-spread), 'blue'))
    else:
        print(colored('Spread de ${} é mais baixo que o Spread Mínimo parametrizado de ${} '.format(spread, spreadMinimo), 'blue'))

def EfetuarCompra():
    global valorCompra
    global valorVenda
    cotacao = RetornarCotacao('MercadoBitcoin', 'BTC/BRL')
    time.sleep(2)
    cotacaoEUA = RetornarCotacao('BitTrex', 'BTC/USDT')
    
    CalcularSpread(cotacao, cotacaoEUA)
    
    if cotacao <= valorCompra:
        print(colored('Comprando 1 Bitcoin a: ' + str(cotacao), 'green'))
        
        valorCompra = cotacao
        valorVenda = valorCompra + margemOperacao
        
        return True
    else:
        print(colored('Aguardando cotação de {} diminuir até {} para comprar!'.format(cotacao, valorCompra), 'red'))
        return False

def EfetuarVenda():
    global valorVenda
    global valorCompra
    cotacao = RetornarCotacao('MercadoBitcoin', 'BTC/BRL')
    time.sleep(2)
    cotacaoEUA = RetornarCotacao('BitTrex', 'BTC/USDT')
    
    CalcularSpread(cotacao, cotacaoEUA)
    
    if cotacao >= valorVenda:
        print(colored('Vendendo 1 Bitcoin a: ' + str(cotacao), 'yellow'))
        
        valorVenda = cotacao
        valorCompra = valorVenda - margemOperacao
        
        return False
    else:
        print(colored('Aguardando cotação de {} aumentar até {} para vender!'.format(cotacao, valorVenda), 'red'))
        return True
