import numpy as np
import pandas as pd
from datetime import datetime
from matplotlib import dates
import matplotlib.pyplot as plt
from mpl_finance import candlestick_ohlc

import exchange

plt.style.use('dark_background')

list = exchange.BuscarOHLCV('BitTrex', 'BTC/USDT', '1d', 1000)
#Estrutura o list do json em um array
data = np.array(list)
data = data.transpose()
#Cria o cabeçalho das colunas
data = {"time":data[0], "open":data[1], "high":data[2], "low":data[3], "close":data[4], "volume":data[5]}
#Converte do tipo 'numpy.ndarray' para o tipo 'pandas.core.frame.DataFrame'
data = pd.DataFrame(data)

data['time'] = data['time'].apply(lambda x: datetime.fromtimestamp(x/1000.0))
data = data.set_index('time')
data['time'] = data.index.map(dates.date2num)

ohlc = data[['time','open','high','low','close']]

ax1 = plt.subplot2grid((6,1), (0,0), rowspan=4, colspan=1)
ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1, sharex=ax1)
ax1.xaxis_date()

candlestick_ohlc(ax1, ohlc.values, colorup='g')
ax2.fill_between(data['volume'].index.map(dates.date2num), data['volume'].values, 0)
plt.show()
