import datetime
import sys

sys.path.append('../')
import Constant
import json
import pandas as pd
import os
import numpy as np
from scipy.optimize import minimize
from scipy.optimize import Bounds
import pprint
'''
	Assumpitons:
		+ volatility has computed with log rule of rate of return 
'''


class Analysis:

	@staticmethod
	def long_run_variance(data : pd.DataFrame()):	
		# Compute the rate of return 
		
		data['TP'] = (data['low']+data['high']+data['close'])/3
		data['return'] =  np.log(data['TP'].copy().shift(-1)/data['TP'])
		return np.square(data['return'].std(ddof=1,skipna=True))
	
	@staticmethod
	def rolling_variance(data : pd.DataFrame(), period : int):
		data['var'] = data['TP'].rolling(window=period).var(ddof=1)
		return data

	@staticmethod
	def MA_SMA(data : pd.DataFrame() , period : int):
		''' The first thing to notice is that by default rolling looks for n-1 prior rows of data to aggregate, 
		where n is the window size. if the condition is not met, it will return NaN '''

		data['MA_'+str(period)] = data['TP'].rolling(window=period).mean()
		data['MA_'+str(period)].fillna(inplace=True,method='backfill')
		data['SMA_' + string(period)] = data['MA_'+str(period)] /data["TP"]	
		
		return data

	@staticmethod
	def EMA(data : pd.DataFrame() ,period : int):

		'''			The first thing to notice is that by default rolling looks for n-1 prior rows of data to aggregate, where n is the window size. 	
						if the condition is not met, it will return NaN		
		'''
		data['EMA_'+str(period)] = data['TP'].ewm(span = period,adjust=True).mean()
		
		diff_price_ewm = []
		for i in range(len(data)):
			diff_price_ewm.append(data["TP"][i] - data['EMA_'+str(period)][int(i/period)])
		data['EMA_'+str(period)+'_var']  = np.square(diff_price_ewm)
		data['EMA_'+str(period)+'_var']  = data['EMA_'+str(period)+'_var'].copy().rolling(window=period).sum()/period

		return data


	def __init__(self, ticker,start_date=datetime.datetime(2020,9,1), end_date=datetime.datetime.now()):
		self.ticker  = ticker.upper()
		self.start_date = start_date
		self.end_date = end_date
		self.var_map =  {}
		self.list_klines = []
		self.data_kline_map  = self.extract_data_map_kline()



	def extract_data_map_kline(self) -> {} :
		data_kline_map = {}
		path = Constant.PATH+'Data/'+self.ticker
		list_files = os.listdir(path)
		list_klines = [ file.split(self.ticker)[1].split('.txt')[0]  for file in list_files ] 
		for kline in list_klines:
			self.var_map[kline] = {}
			data_kline_map[kline] = self.extract_data(kline)
		self.list_klines = list_klines
		return data_kline_map	

	def extract_data(self,kline) -> pd.DataFrame() :
		path = Constant.PATH+'Data/'+self.ticker+'/'+self.ticker+kline+'.txt'
		f = open(path,'r')
		payload = f.read()
		price = json.loads(payload)
		f.close()
	
		for key in price.keys():
			price[key] = np.array(price[key],dtype='f8')

		df = pd.DataFrame(data=price)
		# you cannot use datetime.date.fromtimestamp because it might happen 2020-10-25 00:59:59.999 and 2020-10-25 23:59:59.999
	
		df['closeTime'] = df.closeTime.apply(lambda q :  datetime.datetime.fromtimestamp(q))
		df = df.set_index('closeTime')

		df = df[ df.index >= self.start_date] 
		df = df[ df.index <= self.end_date ] 

		return df
	
	def compute_variance(self,period = 10):	
		# Compute the rate of return 
		for kline in self.list_klines:
			data = self.data_kline_map[kline]
			self.var_map[kline]['Long-Run'] = Analysis.long_run_variance(data)
			data  = Analysis.rolling_variance(data, period)
			self.var_map[kline]['Rolling'] = data['var'][-1]

	# Compute the Moving Average MA
	def compute_MA(self, period):
		for kline in self.list_klines:
			data = self.data_kline_map[kline]
			'''
				The first thing to notice is that by default rolling looks for n-1 prior rows of data to aggregate, where n is the window size. 
				if the condition is not met, it will return NaN
			'''
			data = Analysis.MA_SMA(data,period)
	
	# Compute the Exponential Moving Average EMA	and the rolling volatility with mean = EMA of the period
	
	def compute_EMA(self,period):
		for kline in self.list_klines:
			data = self.data_kline_map[kline]
			data = Analysis.EMA(data ,period)
			self.var_map[kline]['EMA'] = data['EMA_'+str(period)+'_var'][-1]
			
	def Garch_variance_prediction(self):
		#for kline in self.list_klines:
		for kline in ['12h','1d','4h','6h','1h']:	
			data = self.data_kline_map[kline]
			#data = data.drop( [  (col if (col not in ['return','EMA_'+str(period)+'_var']))  for col in data.columns ])
			data.dropna(inplace=True)
			
			def maximize_likelihood(weight):
				alpha = weight[0]
				beta = weight[1]
				w = self.var_map[kline]['Long-Run']*(1 - alpha - beta)
				data['GARCH_var'] = np.array([0 for i in range(len(data))])
				for i in range(len(data)):
					if i==0:	
						data['GARCH_var'][i] =  (data['return'][i])**2
					else:
						data['GARCH_var'][i] = w + beta*data['GARCH_var'][i-1] + alpha*(data['return'][i-1]**2)
				return np.sum( np.log(data['GARCH_var']) + np.square(data['return'])/data['GARCH_var'])

			alpha = 0.5
			beta = 0.5
			weight = [alpha,beta]
			#eq_cons = {'type': 'eq','fun' : lambda x: x[0]+x[1]+x[2] - 1 }
		
       		#  method = 'L-BFGS-B'/'nelder-mead'   [ 2.746e-01  5.714e-01]
       		#
			res = minimize(maximize_likelihood,weight, method = 'SLSQP')	
			self.var_map[kline]['Garch'] = self.var_map[kline]['Long-Run']*(1 - res.x[0] - res.x[1]) + res.x[1]*data['GARCH_var'][-1]  + res.x[0]*(data['return'][-1]**2)
		
	
ticker = "soleth"
period = 10
prova  = Analysis(ticker)
prova.compute_variance()
prova.compute_EMA(10)
data = prova.data_kline_map['1d']
#print(data["TP"])

prova.Garch_variance_prediction()
pprint.pprint(prova.var_map)


