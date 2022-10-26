# Crypto-Trading-Bot
Crypto Trading Bot to buy/sell cryptocurrencies on Binance.com which can run 24/7. Easy to set up with a customisable config.py file. 

In detail, if the conditions based on the chosen trading strategies are met, the running bot would execute a MARKET BUY ORDER and a SELL LIMIT ORDER would be filled regarding the associated rate of profit (Constant.EARNING_MAP). 
# ddff
In addition, it provides the following main services:
- Open Websocket connected through Binance API Management;
- Debug log, saved in "log" folder on a daily basis;
- Wrap-up email sent every day specifying the executed orders and the log file of the current day attached;
- Methods for the construction and updating  Crypto Database (stored in  "Data" folder);
- Methods for Retrieving/Plotting  historical market data for Data Analysis.

Regarding the Crypto Database, we encapsulate the historical market data in JSON format, write a file .txt, and save it in the "Data" folder. Features (for each kline interval):
- CloseTime
- Low/High/Close Price;
- Volume;

The Data Analysis consists of splitting the dataframe containing the historical market data into smaller dataframe. In each shred dataframe, we highlight the minimum close prices  and the values of specific Trading Indicators at the local minimum, such as:

- High/Low/Close Relative Strength Index (RSI);
- Money Flow Index (MFI);
- Exponential Moving Average (EMA) with periods 200, 100, 50, 25, 10.
- Differences between different EMAs and their rate of return respect the current close price.

Then, everything is combined in a unique dataframe which is saved in "Analysis" folder. 

Regarding the plotting, it shows the close price graph and EMAs behaviour at the associated time interval. The plot is saved as .png file in "Photo" folder.

There are implemented three different trading strategies (written in utilities_bot.bot_rsi() method ):
1) "strategy_crash": "displacement_200 > 0.09"
2) "strategy_1": "not strategy_crash   and  rsi_low < RSI_OVERSOLD  and  ema_diff < 0.008 and displacement_200 > 0.06 and displacement_50 > 0.04"
3) "strategy_2" =  "not strategy_crash   and  rsi_low < RSI_OVERSOLD  and  ema_diff > 0.02 and displacement_200 > 0.05 and displacement_50 > 0.03"
		
   where  
   a) "displacement_200" is the rate of return of the Exponential Moving Average with 200 period (ema_200) with the respect to the current close price;
   
   b) "displacement_50" is the rate of return of the Exponential Moving Average with 50 period (ema_200) with the respect to the current close price;
   
   c) "ema_diff" is  (ema_200 - ema_50)/ema_50
   
   d) "rsi_low" is the Relative Strength Index (RSI) of the low prices;
   
   e) the capital VARIABLES are setting constant variables specified in Constant.py.

Possibility to run the bot in a Test mode, with TEST = True.

The remove_file_log.py script deletes every log file in the "log" folder, execept for the log file of today.


The Crypto Trading Bot uses:
- Python 3.9.7
- TA-Lib 0.4.19
- Numpy 1.21.2
- Pandas 1.3.2
- Matplotlib 3.4.3
- Websocket 1.2.3
- Binance 1.0.12
- Binance API












Free to Donate!

Cheers!

-- BTC Wallet --> bc1qnk2xqj29dkqm6nq985j95x744uqf0gqt3646xp

-- ETH Wallet --> 0x347c18Ed43451E9bCa88cB51c7dbfBd2Db9328b5

-- SOL Wallet --> HTSoVVagBFZ4kq9g6C6eqmwLqAeghAR21ZCSWqDNytAS

-- AVAX C-Wallet --> 0x347c18Ed43451E9bCa88cB51c7dbfBd2Db9328b5

-- ATOM Wallet --> cosmos10tlelp6u5x74u3dw58qezt06wc62mu9eft07ll
