

import utilities_test,utilities_bot,utilities,json,math
import pprint
import datetime
import time
import shutil
import numpy as np
import datetime
import talib
import config
from talib import abstract
from binance.client import Client
import config
import pandas as pd
import scipy
from Constant import *
import pandas_datareader as web
import matplotlib.pyplot as plt       

utilities.retrieveDataYear(["ADAUSDT","VETUSDT"],numberOfYear = 3,interval = ["4h"])
coins = ['BTCUSDT','ETHUSDT','AVAXUSDT','SOLUSDT','FTMUSDT','MATICUSDT','ADAUSDT','VETUSDT']
utilities.retrieveDataUpdating(coins,interval = ["4h"])
cc

ticker = 'BTCUSDT'

end = datetime.datetime.now()
start = end - datetime.timedelta(days = 90)
df = web.DataReader('GOLD',data_source="yahoo",start=start, end=end)

plt.figure(figsize=(16,8))
plt.title('Close Price GOLD')
plt.plot(df['Close'])
plt.xlabel("Date",fontsize=18)
plt.ylabel('Close Price USD ($)',fontsize=18)
plt.grid()
#plt.show()
#utilities_test.earningFunction({"rate" :19.4 ,"budget":5000,"fee":0.00})

#utilities.updateDatabase()

#utilities_test.bot_test(list_tickers = [ticker],interval = ['5m'], rsi_period =[14] ,PLOT=True)



#print(abstract.AD)

list_tickers = ["BTCUSDT",
"ETHUSDT",
"ADAUSDT",
"BNBUSDT",
"XRPUSDT",
"SOLUSDT",
"DOGEUSDT",
"DOTUSDT",
"LUNAUSDT",
"AVAXUSDT",
"UNIUSDT",
"LINKUSDT",
"LTCUSDT",
"ALGOUSDT",
"BCHUSDT",
"ATOMUSDT",
"ICPUSDT",
"SHIBUSDT",
"MATICUSDT",
"AXSUSDT",
"FILUSDT",
"XLMUSDT",
"VETUSDT",
"ETCUSDT",
"XTZUSDT",
"FTTUSDT",
"THETAUSDT",
"XMRUSDT"
]
#utilities.retrieveDataUpdating(coins,interval = ['1m','3m','5m','15m','30m','1h','2h','4h','6h','12h','1d'])
#utilities.retrieveData(coins[0:1],howLong = 35,interval = ['1m'],end_date = datetime.datetime(2020,7,30),writeOnFileTrigger = True)
#utilities.retrieveDataUpdating(coins[0:1],interval = ['1m'])
#utilities.retrieveDataYear([ticker],3)



#utilities.retrieveDataYear(coins[5:],1.6,interval = INTERVAL)
#utilities.retrieveDataYear(coins[1:],1)
#utilities_test.plot_crypto(coins,['15m'],start_date = datetime.datetime(2021,8,1),end_date = datetime.datetime(2021,9,1), single_plot=True)
#utilities.bot_test_rsi(list_tickers = list_tickers)

'''

coin_array = []
for i in range(0,int(len(list_coin)/7)+1):
    if(i == int(len(list_coin)/7) ):
        coin_array.append(list_coin[i*7:-1])    
    coin_array.append(list_coin[i*7:(i+1)*7])
count = 0 
for coin in list_coin:
    try:
        if( count == 7):
            count = 0
            time.sleep(300)
        utilities.retrieveData([coin.upper()])
        count = count +1
    except BinanceAPIException as API_error:
        print(coin,'NOT MATCH')


from binance.helpers import round_step_size

tick_size = 0.01
symbol_info =  client.get_symbol_info('SOLEUR')
tick_size = float(json.loads(json.dumps(symbol_info))['filters'][0]['tickSize'])
#balance = utilities.getPrecision(float(balance)/price, PRECISION)
print(tick_size)
rounded_amount = round_step_size(130.456666444, tick_size)
print(rounded_amount)
'''

from binance.enums import *

client = Client(config.API_KEY,config.API_SECRET,tld= 'com')
'''
order = client.create_test_order(
    symbol='USDTRUB',
    side=SIDE_BUY,
    type=ORDER_TYPE_MARKET,
    #timeInForce=TIME_IN_FORCE_GTC,
    #price = 128.22, 
    quantity= 444
    #quoteOrderQty = float(balance)
    )
print(order)
'''
symbol_info =  client.get_symbol_info('BTCUSDT')
step_base = math.log10(1.0/float(json.loads(json.dumps(symbol_info))['filters'][2]['stepSize']))
print(step_base)
print(json.dumps(symbol_info, indent=2))
'''
#client.close_connection()
    
#loop = asyncio.get_event_loop()
#loop.run_until_complete(main())

'''