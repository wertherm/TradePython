import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from matplotlib import ticker, dates #Para usar ticker.MaxNLocator(4) e dates.date2num
from datetime import datetime #Para usar datetime.fromtimestamp

#Módulo descontinuado: https://matplotlib.org/api/finance_api.html
#   from matplotlib.finance import candlestick_ohlc
#
#   Mensagem de erro de descontinuação:
#       warnings.warn(message, mplDeprecation, stacklevel=1) MatplotlibDeprecationWarning: The finance module has been deprecated in mpl 2.0 and will be removed in mpl 2.2. Please use the module mpl_finance instead.
#
#Instalação do módulo mpl_finance (Substituto para o matplotlib.finance)
#   Tem que instalar o módulo mpl_finance forçado "hardcoded" ou seja sem usar o PyPI com o comando 'pip3 install mpl_finance', senão receberá o erro 'Could not find a version that satisfies the requirement mpl_finance'. Prineiro tem que baixar o source em https://github.com/matplotlib/mpl_finance descompactar e depois executar o comando 'python3 setup.py install'.
#
#   Atenção: É muito importante que você entre no diretório dos fontes baixados pelo Terminal, para efetuar a instalação. Por exemplo, se copiou os fontes para Desktop/mpl_finance, no Terminal você deverá apontar o cursor para este diretório com 'cd desktop/mpl_finance', para depois executar 'sudo python3 setup.py install'. E usando 'sudo' na frente do comando de instalação, você habilita os privilégios, assim impossibilitando conflitos de permissão.
#   Se você executar por exemplo 'sudo python3 desktop/mpl_finance/setup.py install' sem estar com o cursor apontado para o diretório 'cd desktop/mpl_finance' no Terminal, os fontes do módulo mpl_finance não serão copiados para os locais corretos de onde são instalados todos os módulos no Python.
#   Provavelmente o módulo mpl_finance será copiado para '/users/werther' no OS X e alguns arquivos essencias do módulo nem serão encontrados e portanto não serão copiados. Quando você tentar usar o módulo com 'from mpl_finance import candlestick_ohlc' no seu código Python, receberá o erro: 'No module named mpl_finance'.
#
#   Depois de realizada a instalação correta do módulo mpl_finance, você pode executar o comando 'pip3 freeze', que você verá o módulo instalado corretamente, também pode usar 'pip3 show mpl_finance' ou 'pip3 show mpl-finance' para ver as informações do módulo. Também pode testar os exemplos contidos em mpl_finance/examples.
#
#Desinstalação do mpl_finance
#   Caso ocorra algum problema durante a instalação é só desinstalar o módulo, com o comando:
#       pip3 uninstall mpl_finance

from mpl_finance import candlestick_ohlc

import exchange

plt.style.use('dark_background') #Estilo da plotagem. Bonitos: bmh, Solarize_Light2
#print(plt.style.available) #['_classic_test', 'bmh', 'classic', 'dark_background', 'fast', 'fivethirtyeight', 'ggplot', 'grayscale', 'seaborn-bright', 'seaborn-colorblind', 'seaborn-dark-palette', 'seaborn-dark', 'seaborn-darkgrid', 'seaborn-deep', 'seaborn-muted', 'seaborn-notebook', 'seaborn-paper', 'seaborn-pastel', 'seaborn-poster', 'seaborn-talk', 'seaborn-ticks', 'seaborn-white', 'seaborn-whitegrid', 'seaborn', 'Solarize_Light2', 'tableau-colorblind10']

#Retorna o tipo 'list' para tabular, popular com o pandas.DataFrame.
#OHLCV não é o OrderBook, mas sim as ultimas ordens que foram executadas e determinaram o preço de abertura, máxima, mínima e fechamento dentro do timeframe parametrizado. Permitindo assim plotar Candlestick Charts.
list = exchange.BuscarOHLCV('BitTrex', 'BTC/USDT', '1d', 10) #Se você parametrizsr o 'limite' para trazer somente 10 registros, serão mostrados apenas os 10 primeiros candles. No caso da Bittrex no timeframe de '1m' são retornados 10 dias atrás até a data atual. Portanto nesse caso serão 14.400 candles (60m*24h*10d), como serão mostrados somente os 10 primeiros, a data deles será de 10 dias atrás até a data atual. Já no timeframe de '1d' serão retornados candles de 3 anos atrás até a data atual.
#json = exchange.BuscarOHLCV('MercadoBitcoin', 'BTC/BRL', '1m') #O MercadoBitcoin não possui dados de OHLCV. Portanto ele é emulado pela biblioteca CCXT. Se você ver através das propriedades exchange.has['fetchOHLCV'] ou exchange.timeframes, receberá o retornado 'emulated'. E sem os dados OHLCV, não é possível fazer análise técnica pelo robô.

#print(type(list))
#Estrutura o list do json em um array
data = np.array(list)
data = data.transpose()

#Cria o cabeçalho das colunas
data = {"time":data[0], "open":data[1], "high":data[2], "low":data[3], "close":data[4], "volume":data[5]}

#Converte do tipo 'numpy.ndarray' para o tipo 'pandas.core.frame.DataFrame'
data = pd.DataFrame(data)

#A atribuição 'data = pandas.DataFrame(data)', deve ficar acima da linha abaixo abaixo. Pois 'data' deve ser do tipo 'pandas.core.frame.DataFrame' e não 'numpy.ndarray', para ter o tratamento abaixo.
data['time'] = data['time'].apply(lambda x: datetime.fromtimestamp(x/1000.0)) #É necessário para não ocorrer o erro: AttributeError: 'float' object has no attribute 'toordinal'. Pode usar .fromtimestamp ou .utcfromtimestamp o resultado será o mesmo.
data = data.set_index('time') #Troca a coluna de indíce ordinal padrão por time.

#print(data.values)
#print(data)
#dates.IndexDateFormatter(data.index.map(dates.date2num), '%d. %b %Y')
data['time'] = data.index.map(dates.date2num) #Corrige o erro: KeyError: "['time'] not in index". E precisa da linha 'data = data.set_index('time')' acima, senão também ocorrerá o erro: AttributeError: 'int' object has no attribute 'toordinal'
#--ohlc = data[['time','open','high','low','close']]
#print(data)

#dataArray = [('2016-03-10 21:00:00', '420.220000', '490.220000', '350.000000', '397.020000'),
#             ('2016-03-11 21:00:00', '397.099990', '455.810000', '397.099990', '414.810000'),
#             ('2016-03-12 21:00:00', '397.100000', '415.460000', '397.099990', '415.460000')]

#ohlc = dataArray[[0,1,2,3,4]]

#ohlc_data = []

#for line in dataArray:
#    ohlc_data.append((dates.datestr2num(line[0]), np.float64(line[1]), np.float64(line[2]),
#                      np.float64(line[3]), np.float64(line[4])))

fig, ax = plt.subplots() #Usar 'fig' resolve o erro: AttributeError: 'tuple' object has no attribute 'add_line'. E pode ser qualquer texto ao invés de 'fig'. 'fig' é apenas uma convenção para 'figure' do módulo matplotlib.

#Primeira Plotagem (OHLC):
#--candlestick_ohlc(ax, ohlc.values, colorup = 'g', colordown = 'r') #Se mudar 'ohlc.values' para somente 'ohlc', irá ocorrer o erro: ValueError: not enough values to unpack (expected 5, got 4)
#candlestick_ohlc(ax, dates.datestr2num(data['time'].values), np.float64(data['open']), np.float64(data['high']), np.float64(data['low']), np.float64(data['close']))

#Segunda Plotagem (Volume):
#A primeira plotagem 'candlestick_ohlc' causa conflito com esta
#data.plot(y=['volume'])
bars = dates.num2date(data['time']) #dates.num2date(data['time']) ou data['time'].apply(lambda x: datetime.fromtimestamp(x/1000.0)) ou data['time'].dt.strftime('%d. %b %Y')
height = data['volume'] #Altura das barras
width = 0.8 #Largura das barras, não funciona corretamente, quando tem muitas barras.
print(bars)
print(height)
y_pos = np.arange(len(bars)) #Atribui a quantidade de barras
# Create bars
plt.bar(y_pos, height, width, color="blue")
# Create names on the x-axis
plt.xticks(y_pos, bars) #A data deve ser um índice, para que acompanhe o gráfico

fig.autofmt_xdate() #Inclina as datas

#ax.set_xticklabels(bars)
#ax.xaxis_date()
#ax.grid() #Insere uma grade no gráfico
ax.xaxis.set_major_locator(ticker.MaxNLocator(4)) #Limita a quantidade de labels no eixo X
#ax.xaxis.set_major_formatter(dates.DateFormatter('%d. %b %Y')) #Formata os dados do eixo X como data

plt.show()
