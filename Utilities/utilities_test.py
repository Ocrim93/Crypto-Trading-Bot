import Utilities.utilitiesFunction as utilities
import Utilities.utilities_bot as  utilities_bot
from Constant import *
import datetime
import json,time
import numpy as np
import matplotlib.pyplot as plt  
import talib
import pandas as pd 
import math
import random 
import pprint


colors = ['#1F77B4']

''' Method to plot crypto graph trending  
	Features:
		++ Plot more coins and different Kindle periods, single Plot or Multi Plot
		++ Choose Start Date and End Date
		++ Build a Trading Indicators Dataframe and write in a file stored in "Analysis" folder 

'''
def plot_crypto(list_tickers,list_kline,rsi_period=14, start_date=datetime.datetime(2020,9,1), end_date=datetime.datetime.now(),days = 0,single_plot=True ):

	df_array = []
	title_list = []
	for ticker in list_tickers:
		for kline in list_kline:
			if single_plot:
				df_tuple = extract_data(ticker,kline,rsi_period, start_date, end_date,days )
				plotting(ticker,kline,rsi_period,df_tuple[0],df_tuple[1])
				continue
			df = extract_data(ticker,kline,rsi_period, start_date, end_date,days )[0]
			title = ticker + '    with   ' + kline 
			df_array.append(df)
			title_list.append(title)
	if not single_plot:		
		multi_plot(title_list,df_array)			


def extract_data(ticker,kline,rsi_period, start_date=datetime.datetime(2020,9,1), end_date=datetime.datetime.now(),days = 0 ):
	pd.set_option('display.max_rows',None)
	pd.set_option('display.max_columns', None)
	pd.set_option('display.width', None)
	pd.set_option('display.max_colwidth', None)
	
	if days !=0:
		start_date = end_date - datetime.timedelta(days)
		
	# Extract stored Data from built crypto Database 
	path = PATH+'Data/'+ticker+'/'+ticker+kline+'.txt'
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

	
	#Indicators
	df = indicators(df.copy(),rsi_period)
	df = df[ df.index >= start_date] 
	df = df[ df.index <= end_date ] 
	
	# Locate the local minimum
	df_minimum = find_minimum(df)
	
	# build a DataFrame to write on file
	df_on_file = build_DataFrame_to_write_on_file(df.copy(),df_minimum)
	
	# write on file and save in "Analysis" folder 
	write_DataFrame_on_file(df_on_file,ticker,kline,rsi_period,df.index[0],df.index[-1])
		
	return df,df_minimum

#Compute the Trading indicators 
#Insert into DataFrame

def indicators(df,rsi_period):

	df['rsi_high'] = talib.RSI(df['high'], rsi_period)
	df['rsi_low'] = talib.RSI(df['low'], rsi_period) 
	df['rsi_close'] = talib.RSI(df['close'], rsi_period)
	df['mfi'] =talib.MFI(df['high'],df['low'],df['close'],df['volume'], timeperiod=rsi_period) 
	
	for ema in EMA_LIST:
		df[ema] = talib.EMA(df['close'],timeperiod=int(ema.replace('ema_','')))
	return df


# Construction Local Minimum Dataframe 

def find_minimum(df):
	df_minimum  = pd.DataFrame()
	minimum = []
	index_minimum = []

	for item in np.array_split(df,NUMBER_OF_MINIMUM):
		if len(item) ==0:
			continue
		minimum.append(item['close'].min())
		index_minimum.append(item['close'].idxmin())  #if you find a minimum along the index column use idxmin()
		
	df_minimum['minimum'] = minimum
	df_minimum['closeTime'] = index_minimum
	#df_minimum = df_minimum.set_index('date')

	return df_minimum
# Formatting the dataframe to write on file
def build_DataFrame_to_write_on_file(df_on_file,df_minimum):
	df_on_file = df_on_file.loc[df_minimum['closeTime']]
	df_on_file = compute_differences(df_on_file.copy())
	df_on_file.reset_index(inplace=True)
	df_on_file.closeTime = df_on_file.closeTime.apply(lambda x : x.date())
	columns = df_on_file.axes[1]

	return df_on_file

# Write the dataframe on a file
def write_DataFrame_on_file(df_on_file,ticker,kline,rsi_period,start,end):
	dir_path =  PATH+'Analysis/'
	columns = df_on_file.axes[1]
	splitting_number = int(len(columns)/8)
	for i,item in enumerate(np.array_split(df_on_file,splitting_number,axis=1)):
		path = dir_path + str(datetime.datetime.now().strftime('%Y-%m-%d'))+'#'+str(i)+'.txt'
		utilities.writeOnFile(dir_path,path,pd.DataFrame(item),ticker=ticker,kline=kline,rsi_period=rsi_period,start = start,end = end )
	print('WRITING ON FILE OK!')	
	
def plotting(ticker,kline,rsi_period,df,df_minimum):
	#pd.set_option('display.max_rows',None)
	#pd.set_option('display.max_columns', None)
	#pd.set_option('display.width', None)
	#pd.set_option('display.max_colwidth', None)
	string_date =  str(df.index[0].date()) + '  to ' +  str(df.index[-1].date()) + '   ' + str(df.index[-1] - df.index[0])
	title = ticker + '    with   ' + kline + '  rsi_period: '+ str(rsi_period) +'   from  ' +string_date
	
	plt.figure(figsize=(16,8))
	plt.title(title)
	plt.ylabel('Price',fontsize=18)
	plt.xlabel("Time " ,fontsize=18)

	# Plotting the close price
	plt.plot(df.index  ,df.close,color= '#1f77b4')

	#Plotting the EMA lines with different colours
	for ema in EMA_LIST:
		if(ema in EMA_LIST_SKIP): continue 
		plt.plot(df.index ,df[ema], color = generator_colour())
	
	#Create a legend 
	legend_list = list(['price'])
	plt.legend(legend_list + EMA_LIST)

	#Mark the local minimum 

	plt.scatter(df_minimum['closeTime'],df_minimum['minimum'],marker = 'o',color = generator_colour())
	for row  in df_minimum.itertuples():
		plt.annotate(row[0],(row[2],row[1]),xytext = (row[2],row[1]*0.95))
	
	plt.grid()
	plt.show(block=False)
	# Save the plot in Photo folder 
	plt.savefig(PATH+'Photo/'+ticker + '.' + kline + '.'+ str(rsi_period)+'.png')
	plt.pause(30)
	plt.close('all')

# Method to enable a Multi Plot
def multi_plot(title_list,df_array):
	plt.figure(figsize=(18,8))
	plt.suptitle('from  ' + str(df_array[0].index[0].date()) + '  to ' +  str(df_array[0].index[-1].date()) + '   ' + str(df_array[0].index[-1] - df_array[0].index[0]),fontweight="bold",fontsize = 12) 
	division_plot = how_to_divide_multi_plot(len(title_list))

	plots = [plt.subplot(division_plot+i) for i in range(len(title_list)) ]
	for i,df in enumerate(df_array):
		plots[i].set_title(title_list[i],fontsize=9)
		plots[i].grid(True,which='major')
		plots[i].plot(df.index ,df.close,color= generator_colour())
	
	plt.show(block=False)
	# Save the plot in Photo folder 
	plt.savefig(PATH+'Photo/set.png')
	plt.pause(10)
	plt.close('all')

def compute_differences(df):
	
	for ema in EMA_LIST:
		column_name = 'displ_'+str(ema.replace('ema_',''))+ ' (%)'
		df[column_name] = (df[ema] - df['close'])/df['close']*100
	
	df['200-100'] = df['ema_200'] - df['ema_100']
	df['200-50'] = df['ema_200'] - df['ema_50']
	df['200-25'] = df['ema_200'] - df['ema_25']
	df['100-50'] = df['ema_100'] - df['ema_50']
	df['100-25'] = df['ema_100'] - df['ema_25']
	
	return df

# Generator of random color for the plotting 

def generator_colour():
	global colors
	
	color =  '#' + ''.join([random.choice('ABCDEF0123456789') for i in range(6)]) 
	if color in colors:
		generator_colour()
	else:
		colors.append(color)	
		return color 

#Divide the dataframe in shred dataframes to study the trading indicators at local minimum

def how_to_divide_multi_plot(n):
	row = 1
	column = 1
	increase = True
	
	while row*column < n:
		if increase:
			row = row + 1
			increase = False
		else:
			increae = True
			column = column + 1 

	return int(str(row)+str(column) + str(1))

