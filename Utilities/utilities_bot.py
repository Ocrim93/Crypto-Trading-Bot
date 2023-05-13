from Constant import *
import Constant
import talib
import config
from binance.client import Client
from binance.enums import *
from  binance.exceptions import *
import Utilities.utilitiesFunction as utilities
import numpy as np
import pprint 
from talib import stream
from binance.helpers import round_step_size
import datetime
import traceback,sys
import math


# Method to format and Fill/Execute BUY/SELL ORDERS
def market_order(bot_map,TEST):

	market_order = bot_map
	market_order['outcome'] = False
	if TEST:
		market_order = market_order_test(market_order)
		summary_book = market_order['summary_book']+1 
		market_order['outcome'] = True
		market_order['summary_book'] = summary_book
		
		
	else:
		try:
			message_log = 'Error '
			order_buy = {}
			
			# Make a connection with a Binance Account through API
			client = Client(config.API_KEY,config.API_SECRET,tld= 'com')
			
			# Execute BUY MARKET ORDER
			order_buy = client.order_market_buy( symbol= TRADE_SYMBOL, quoteOrderQty= utilities.getPrecision(bot_map['TRADE_QUANTITY_QUOTE'],STEP_QUOTE))
			
			# Check the status of the BUY MARKET ORDER and retrieve the information 
			if(order_buy['status'] !='FILLED'):
				raise Exception('MAKER ORDER NOT FILLED')
			else:
				order = checkExecutionOrder(order_buy['orderId'])

				order['price'] = str(order_buy['fills'][0]['price'])

				price_bought = float(order['price'])
				TRADE_QUANTITY_BASE = bot_map['TRADE_QUANTITY_BASE'] + float(order['executedQty']) 
				TRADE_QUANTITY_QUOTE = bot_map['TRADE_QUANTITY_QUOTE'] - float(order['cummulativeQuoteQty'])
				price_to_sell = str(round_step_size( price_bought*(Constant.EARNING), Constant.TICK_SIZE))

				# Create LIMIT SELL ORDER
				order_to_sell = client.create_order(
    				symbol=TRADE_SYMBOL,
   					side=SIDE_SELL,
   					type= ORDER_TYPE_LIMIT,
   					timeInForce=TIME_IN_FORCE_GTC,
    				price = price_to_sell, 
    				quantity= TRADE_QUANTITY_BASE,
    				)
				orderId = order_to_sell['orderId']	
				
				page = formatting_page(order,TRADE_QUANTITY_BASE,TRADE_QUANTITY_QUOTE)
				bot_map['summary_book'].append(page)
				summary_book = bot_map['summary_book']


		except BinanceAPIException as API_error:
			utilities.log('Binance API Exception' , OUTCOME_KO + str(API_error) )
			return market_order
		
		except BinanceOrderException as order_error:
			utilities.log('Binance Order Exception' , OUTCOME_KO + str(order_error) )
			return market_order

		except Exception as e:
			utilities.log(message_log , OUTCOME_KO + str(e) )
			exc_type, exc_obj, exc_tb = sys.exc_info()
			utilities.log('Detail : \n',str(traceback.extract_tb(exc_tb)))
			return market_order
			

		market_order['outcome'] = True
		market_order['TRADE_QUANTITY_QUOTE'] = TRADE_QUANTITY_QUOTE
		market_order['TRADE_QUANTITY_BASE'] = TRADE_QUANTITY_BASE
		market_order['summary_book'] = summary_book
		market_order['orderId_to_sell'] = orderId
		market_order['price_to_sell'] = float(price_to_sell)


	return market_order

#Method only in a TEST mode	

def market_order_test(bot_map):

	price_bought = bot_map['close_price']
	quantity = utilities.getPrecision(bot_map['TRADE_QUANTITY_QUOTE']/bot_map['close_price'],Constant.STEP_BASE)
	TRADE_QUANTITY_BASE = bot_map['TRADE_QUANTITY_BASE'] + quantity
	TRADE_QUANTITY_QUOTE = bot_map['TRADE_QUANTITY_QUOTE'] - quantity*bot_map['close_price']


	bot_map['TRADE_QUANTITY_QUOTE'] = TRADE_QUANTITY_QUOTE
	bot_map['TRADE_QUANTITY_BASE'] = TRADE_QUANTITY_BASE
	bot_map['price_to_sell'] = price_bought*Constant.EARNING
	
	return bot_map

def bot_rsi(price, in_position,orderId,price_to_sell,TRADE_QUANTITY_QUOTE,TRADE_QUANTITY_BASE,summary_book,rsi_period = RSI_LENGTH,TEST = False):
	
	order_succeeded = {}
	length = len(price['close'])

	#Construction the order map
	order_succeeded['in_position'] = in_position
	order_succeeded['price_to_sell'] = price_to_sell
	order_succeeded['TRADE_QUANTITY_QUOTE'] = TRADE_QUANTITY_QUOTE
	order_succeeded['TRADE_QUANTITY_BASE'] = TRADE_QUANTITY_BASE
	order_succeeded['summary_book'] = summary_book
	order_succeeded['orderId_to_sell'] = orderId
	
	# Needed Check, otherwise most of trading indicators are nan
	if length > EMA_PERIOD:
		
		close_price = price['close'][-1]

		if TEST:
			order_succeeded['close_price'] = close_price

		#Compute trading indicators

		# Compute RSI,MFI, STOCH
		rsi_high = talib.RSI(price['high'], rsi_period)[-1]
		rsi_low = talib.RSI(price['low'], rsi_period)[-1]
		rsi_close = talib.RSI(price['close'], rsi_period)[-1]
		
		mfi = talib.MFI(price['high'],price['low'],price['close'],price['volume'], timeperiod=rsi_period)[-1]
		
		fastk,fastd = stream.STOCH(price['high'],price['low'],price['close'], rsi_period,3, 0, 3, 0)
		fastj = D_WEIGHT*fastd - K_WEIGHT*fastk
		
		fastk,fastd = stream.STOCHF(price['high'],price['low'],price['close'], rsi_period,3, 0)
		rsi_k,rsi_d = stream.STOCHRSI(rsi,timeperiod=rsi_period)
		
		#Compute EMA
		
		ema_200 = talib.EMA(price['close'],timeperiod=200)[-1]
		ema_25 = talib.EMA(price['close'],timeperiod=25)[-1]
		ema_50 = talib.EMA(price['close'],timeperiod=50)[-1]
		
		#Manipulation of trading indicators

		displacement_200  = (ema_200 - price['close'][-1])/price['close'][-1]
		displacement_25  = (ema_25 - price['close'][-1])/price['close'][-1]
		displacement_50  = (ema_50 - price['close'][-1])/price['close'][-1]
		ema_diff =  (ema_200 - ema_50)/ema_50
		
		displ_sequence = displacement_200 > 0.06 and displacement_50 > 0.04 and displacement_25 > 0.03
		rsi_sequence = rsi_close < rsi_low
		
		# Write in the log the value of the main trading indicators in order to analyse later on
		if not TEST:
			utilities.log('close_price',str(close_price))
			utilities.log('rsi ',str(last_rsi)+ ' '+str(fastd)+ ' '+str(fastk)+ ' '+str(fastj)+ ' '+str(rsi_stoch))	

		#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% TRADING STRATEGY %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
		
		# Implementation of 3 different kind of Trading Strategies 
		
		strategy_crash = displacement_200 > 0.09
		strategy_1 =  not strategy_crash   and  rsi_low < RSI_OVERSOLD  and  ema_diff < 0.008 and displacement_200 > 0.06 and displacement_50 > 0.04
		strategy_2 =  not strategy_crash   and  rsi_low < RSI_OVERSOLD  and  ema_diff > 0.02 and displacement_200 > 0.05 and displacement_50 > 0.03
		
		# Chech if there are the conditions for a specific trading strategy

		if  (strategy_1 or strategy_crash or strategy_2) and  in_position:
			if Constant.MINIMUM_AMOUNT == 0.0 :
				Constant.MINIMUM_AMOUNT = utilities.getPrecision(TRADE_QUANTITY_QUOTE/close_price,Constant.STEP_BASE)
				#Constant.FIRST_BUYING = False
				check_right_amount_to_sell = True
			else:
				check_right_amount_to_sell = (Constant.MINIMUM_AMOUNT < utilities.getPrecision(TRADE_QUANTITY_QUOTE/close_price,Constant.STEP_BASE))
			
			# Specific rate of profit depending on the trading strategy
			if check_right_amount_to_sell :
				if strategy_crash:
					Constant.EARNING = EARNING_MAP['big']
				else:
					Constant.EARNING = EARNING_MAP['short']
				
				# Execute a BUY MARKET ORDER and fill a SELL LIMIT ORDER
				order_succeeded = market_order(order_succeeded,TEST)
				if order_succeeded['outcome']:
					order_succeeded['in_position'] = False

	return	order_succeeded			
			
# Formatting Method to update the summary book needed for taking trace of the BUY/SELL ORDERS 

def formatting_page(order,TRADE_QUANTITY_BASE,TRADE_QUANTITY_QUOTE):

	page = {'symbol':'','side': '','type':'','place_time':'','filled_time':'', 'quantity_base': 0.0, 'quantity_quote': 0.0,'price':0.0,'commission':''}
	
	page['symbol'] = order['symbol']
	page['side'] = order['side']
	page['type'] = order['type']
	page['place_time']= datetime.datetime.fromtimestamp(int(order['time'])/1000)
	page['filled_time']= datetime.datetime.fromtimestamp(int(order['updateTime'])/1000)
	page['price']= order['price']
	page['quantity_base'] =  TRADE_QUANTITY_BASE
	page['quantity_quote'] =  TRADE_QUANTITY_QUOTE
	#page['commission'] = str(order['fills'][0]['commission']) +' '+ str(order['fills'][0]['commissionAsset'])
	message_log = order['side'] +'  '+ order['symbol'] + ' price ' +str(order['price'])+ '  TRADE_QUANTITY = ( ' + str(TRADE_QUANTITY_QUOTE) +' , '+ str(TRADE_QUANTITY_BASE) + ' )'
	utilities.log(message_log,OUTCOME_OK)
	
	return page


def checkExecutionOrder(orderId):
	
	client = Client(config.API_KEY,config.API_SECRET,tld= 'com')
	order = client.get_order(symbol = TRADE_SYMBOL,orderId=orderId)
	if order['status'] == 'FILLED':
		return order
	else:
		utilities.log('LIMIT ORDER NOT FILLED', OUTCOME_KO)	
		return {}

def CLV(price):
	return price['volume']/1000.0*((price['close']- price['low'])-(price['high']- price['close']))/(price['high']- price['low'])



