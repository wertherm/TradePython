import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates
import numpy as np
import pandas as pd

import exchange

style.use('ggplot')

list = exchange.BuscarOHLCV('BitTrex', 'BTC/USDT', '1d', 100)
#Estrutura o list do json em um array
data = np.array(list)
data = data.transpose()
#Cria o cabeçalho das colunas
data = {"time":data[0], "open":data[1], "high":data[2], "low":data[3], "close":data[4], "volume":data[5]}
#Converte do tipo 'numpy.ndarray' para o tipo 'pandas.core.frame.DataFrame'
df = pd.DataFrame(data)

df_ohlc = df['close']#.resample('10D').ohlc()
df_volume = df['volume']#.resample('10D').sum()

df_ohlc.reset_index()
df_ohlc['time'] = df_ohlc['time'].map(mdates.date2num)

ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1, sharex=ax1)
ax1.xaxis_date()

candlestick_ohlc(ax1, df_ohlc.values, width=5, colorup='g')
ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values, 0)
plt.show()
