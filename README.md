# Crypto-Trading-Bot
Crypto Trading Botto buy/sell cryptocurrencies on Binance.com that can run 24/7. In detail, if there are the conditions based on the chosen trading strategies, the running bot would execute a MARKET BUY ORDER on Binance and a SELL LIMIT ORDER wwould be filled regarding the associated rate of profit (Constant.EARNING_MAP). 

There are implemented three different trading strategies (written in utilities_bot.bot_rsi() method ):
1) "strategy_crash": "displacement_200 > 0.09"
2) "strategy_1": "not strategy_crash   and  rsi_low < RSI_OVERSOLD  and  ema_diff < 0.008 and displacement_200 > 0.06 and displacement_50 > 0.04"
3) "strategy_2" =  "not strategy_crash   and  rsi_low < RSI_OVERSOLD  and  ema_diff > 0.02 and displacement_200 > 0.05 and displacement_50 > 0.03"
		
   where  
   a) "displacement_200" is the rate of return of Exponential Moving Average with 200 period (ema_200) with the respect to the current close price;
   
   b) "displacement_50" is the rate of return of Exponential Moving Average with 50 period (ema_200) with the respect to the current close price;
   
   c) "ema_diff" is  (ema_200 - ema_50)/ema_50
   
   d) "rsi_low" is the Relative Strength Index (RSI) of the low prices;
   
   e) the capital VARIABLES are setting constant variables specified in Constant.py.


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
