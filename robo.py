# -*- coding: utf-8 -*-
#Resolve o problema de enconding "SyntaxError: Non-ASCII character '\xc3'

#Executando com Python 3 no Mac
#python3 desktop/robo/robo.py

import time

import coinMCAP
import pingpong

#Constantes
flagComprado = False

#Observações
#Você desenvolveu este robô sem depurar, 'debugar'. Assim precisou testar cada posibilidade, rodando o robô diversas vezes e conferindo cada saída e erro que ocorria um a um, para depois ir tratando cada problema. Rascunhar um fluxograma também o ajudou a abstrair melhor a lógica.
#O primeiro robô em C#, você demorou 4 meses para desenvolver. O segundo robô em NodeJS, foram 3 meses. E este em Python, você levou 1 mês.

#1 hora tem 12 ciclos de 5 minutos, em 24 horas são 288 ciclos. Mas nem sempre a cada 5 minutos haverá uma variação de $20 no Bitcoin. Assim da para se basear que o algoritimo executará ordens de compra e venda em pelo menos 100 ciclos.
ciclo = 1
while ciclo <= 288:
    coinMCAP.CoinMarketCap()
    
    if not flagComprado:
        flagComprado = pingpong.EfetuarCompra()
    elif flagComprado:
        flagComprado = pingpong.EfetuarVenda()

    time.sleep(300) #5x60 segundos = 300 segundos ou 5 minutos
    ciclo += 1
