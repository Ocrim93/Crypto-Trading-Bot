import os 
import Constant
from binance.client import Client
import pandas as pd
import datetime, time 
import config
from  Constant import *
import numpy as np 
import json 
import talib
import math
import sendEmail
import asyncio
import pprint
import requests

#%%%%%%%%%%%%%%%%%%%% Method to send a daily wrap-up email %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 

def send_summary_email(summary_book):
	commission_fee = 999
	try:
		client = Client(config.API_KEY,config.API_SECRET,tld= 'com')
		commission_fee = client.get_asset_balance(asset='BNB')['free']
	except BinanceAPIException as API_error:
		log('Binance API Exception' , OUTCOME_KO + str(API_error) )
	finally:		
		today = datetime.datetime.now()
		yesterday  = today - datetime.timedelta(days=1)
		symbol = ''
		message ='BNB LEFT:   '+ str(commission_fee) + '\n'
		subject = TRADE_SYMBOL+ ' (' +PERIOD +') - Daily Wrap-Up '+yesterday.strftime('%d-%m-%Y') 

		if(len(summary_book) == 0):
			message = message + 'No Order Performed Today'
	
		else:
			for page in summary_book:
				message = message + '-------------------------------------------------------'+'\n'
				for key in page.keys():
					message = message + key + ' : ' +str(page[key]) +'\n'
					
				message = message + '-------------------------------------------------------'+'\n'
	

		if sendEmail.sendNotification(subject,message):
			log('Sending email daily wrap-up', OUTCOME_OK)
		else:
			log('Sending email daily wrap-up', OUTCOME_KO)

#%%%%%%%%%%%%%%%%%%%% Method to send a daily wrap-up email %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%		

def log(message,outcome):
	dt = datetime.datetime.now()
	path = PATH+'log/'+ dt.strftime('%d-%m-%Y')+'.txt'

	#path = '/home/pi/Desktop/Binance/Bot/bot'+str(bot_number)+'/log/'+ dt.strftime('%d-%m-%Y')+'.txt'
	if(os.path.exists(path)):
		f = open(path,'a')
	else:
		f = open(path,'w')	
	f.write(str(dt) +'   '+ message+ ' : ' + outcome+'\n')
	f.close()

#%%%%%%%%%%%%%%%%%%%% Method to update your crypto Database  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Check the Data folder and update the historical data by updating the file in each crypto-coin folders

def updateDatabase():
	list_tickers = os.listdir(PATH+'Data/')
	list_tickers.remove('.DS_Store')
	retrieveDataUpdating(list_tickers)

def retrieveDataYear(list_tickers,numberOfYear = 1,interval = []):
	if interval == []:
		retrieveData(list_tickers,howLong = numberOfYear*365,interval = INTERVAL1, writeOnFileTrigger = True)
		retrieveData(list_tickers,howLong = numberOfYear*365,interval = INTERVAL2, writeOnFileTrigger = True)
	else:
		retrieveData(list_tickers,howLong = numberOfYear*365,interval = interval, writeOnFileTrigger = True)	

def retrieveDataUpdating(list_tickers,interval = INTERVAL1+INTERVAL2):

	for ticker in list_tickers:
		dir_path = PATH+'Data/'+ticker+'/'
		for period in interval:
			path = dir_path+ticker+period+'.txt'
			if not os.path.exists(path):
				print(ticker,period,'Not retrieved yet!')
				print('Please run utilities.retrieveData()')
			else:
				f = open(path,'r')
				payload = f.read()
				price = json.loads(payload)
				f.close()
				for key in price:
					price[key] = np.array(price[key],dtype='f8')

				last_date = datetime.datetime.fromtimestamp(price['closeTime'][-1])  
				
				start_date = datetime.datetime(last_date.year,last_date.month,last_date.day)
				start_date_timestamp = datetime.datetime.timestamp(start_date)
				
				df = pd.DataFrame(data=price)
				df = df[df['closeTime'] <  start_date_timestamp ]

				for key in price:
					price[key] = np.array(df[key],dtype='f8')
				days = (datetime.datetime.now() - start_date).days
				
				if days > 0:
					adding_data = retrieveData([ticker],howLong=days, interval = [period])
					for key in price:
						price[key] = np.concatenate((df[key],adding_data[key]),axis=None)
						price[key] = price[key].tolist()
				
					writeOnFile(dir_path,path,price)
					print(ticker,period,' UPDATED!')
				else:
					print(ticker,period,' File already updated!')	




def getHistoricalData(symbol,interval,untilThisDate,howLong=30):

	
	sinceThisDate= untilThisDate - datetime.timedelta(days=howLong)
	sinceThisDate = datetime.datetime(sinceThisDate.year,sinceThisDate.month,sinceThisDate.day)

	sinceThisDate_timestamp = datetime.datetime.timestamp(sinceThisDate)
	untilThisDate_timestamp = datetime.datetime.timestamp(untilThisDate)
	
	

	# Execute the query from Binance - timestamps must be converted to strings !
	try:
		client = Client(config.API_KEY,config.API_SECRET,tld= 'com')
		candle = client.get_historical_klines(symbol,interval,str(sinceThisDate),str(untilThisDate))
	except requests.exceptions.ReadTimeout as timeErr:
		print('timeErr',timeErr)
		time.sleep(10)
		candle = getHistoricalData(symbol,interval,untilThisDate,howLong)
	except requests.exceptions.ConnectionError as connErr:
		print('connErr',connErr)
		time.sleep(60)
		candle = getHistoricalData(symbol,interval,untilThisDate,howLong)
	
	df = pd.DataFrame(candle,columns=['dateTime', 'open', 'high', 'low', 'close', 'volume', 'closeTime', 'quoteAssetVolume', 'numberOfTrades', 'takerBuyBaseVol', 'takerBuyQuoteVol', 'ignore'])
	df.closeTime = df.closeTime.apply(lambda q : float(q/1000))
	
	df = df[df.closeTime >= sinceThisDate_timestamp]
	df = df[df.closeTime < untilThisDate_timestamp]
	
	df = df.drop(['dateTime', 'quoteAssetVolume', 'numberOfTrades', 'takerBuyBaseVol','takerBuyQuoteVol', 'ignore'], axis=1)
	
	return df

def retrieveData(list_tickers,howLong=30, interval = INTERVAL,end_date = datetime.datetime.now(),writeOnFileTrigger = False):
	
	price = {'low': [], 'high':[],'close':[],'volume':[],'closeTime':[]}
	rest = 0
	cycle = 0 
	starting_end_date = end_date 
	if howLong == 0 :
		print('No Retrieved')
		return 0
	if howLong <=30:
		rest = howLong
	else:
		cycle = int(howLong/30.)
		rest = howLong % 30
			
	for ticker in list_tickers:
		dir_path = PATH+'Data/'+ticker+'/'
		for period in interval:
			for key in price.keys():
				price[key] = np.array([],dtype='f8')
			while cycle > 0 :
				df = getHistoricalData(ticker,period,end_date)
				for key in price.keys():
					price[key] = np.concatenate((np.array(df[key],dtype='f8'),price[key]),axis=None)
				
				end_date = end_date - datetime.timedelta(days=30)
				end_date = datetime.datetime(end_date.year,end_date.month,end_date.day)
				cycle = cycle  - 1
			if rest > 0:
				df = getHistoricalData(ticker,period,end_date,howLong=rest)
				for key in price.keys():
					price[key] = np.concatenate((np.array(df[key],dtype='f8'),price[key]),axis=None)
					
			if writeOnFileTrigger:
				for key in price.keys():
					price[key] = price[key].tolist()
				path = dir_path+ticker+period+'.txt'
				writeOnFile(dir_path,path,price)
				
			#initialization for the next period	
			cycle = int(howLong/30)
			end_date = starting_end_date
			
			print(ticker,period,' DONE!')
			#time.sleep(60)
	return 	price

def writeOnFile(dir_path,path,price,**kwargs):

	if(not os.path.exists(dir_path)):
		os.makedirs(dir_path)
	f = open(path,'w')		
	if isinstance(price,pd.DataFrame):
		string_date =  '    from    '+str(kwargs['start'].date()) + '  to ' +  str(kwargs['end'].date()) + '   ' + str(kwargs['end'] -kwargs['start'])
		f.write( kwargs['ticker'] + '    with   ' + kwargs['kline'] + '  rsi_period: '+ str(kwargs['rsi_period'])+ string_date+'\n')
		f.write('\n')
		#price['closeTime'] = price['closeTime'].apply(lambda q : q.strftime('%d-%m-%Y'))
		price.style.set_properties(**{'font-size': '10px'}) 
		payload  = price.to_string()
	else:	
		payload = json.dumps(price).strip()
	
	f.write(payload)
	f.close()

def getPrecision(value, precision):
	
	zeros = pow(10.0,precision)
	return math.floor(value*zeros)/zeros

def setTICKandSTEPvalue(symbol = TRADE_SYMBOL):
	client = Client(config.API_KEY,config.API_SECRET,tld= 'com')
	symbol_info =  client.get_symbol_info(symbol)
	
	tick_size = float(json.loads(json.dumps(symbol_info))['filters'][0]['tickSize'])

	step_base = math.log10(1.0/float(json.loads(json.dumps(symbol_info))['filters'][2]['stepSize']))
	
	Constant.STEP_BASE = step_base
	Constant.TICK_SIZE = tick_size
	











