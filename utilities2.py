import requests
from bs4 import BeautifulSoup 
import os
import utilities


def retrieveSymbolforMarketCap(url ='https://www.coingecko.com/en',second_call=True ):

	path ='/Users/mirco/Desktop/101/Binance/Bot/token_list.txt'
	s = requests.Session()
	page = s.get(url,timeout=260)
	soup = BeautifulSoup(page.content,"html.parser")
	symbol_a = soup.find_all('a', attrs= {"class":"d-lg-none font-bold"})
	
	stablecoin_list = retrieveStableCoin()

	if(os.path.exists(path)):
		f = open(path,'a')
	else:
		f = open(path,'w')	
	for symbol in symbol_a:
		symbol= symbol.text.strip()
		if(symbol in stablecoin_list):
			continue 
		else:
			f.write(symbol)	
			f.write('\n')
	f.close()
	if second_call:
		retrieveSymbolforMarketCap('https://www.coingecko.com/en?page=2',False)
   
def retrieveStableCoin():
	s = requests.Session()
	page = s.get('https://www.coingecko.com/en/categories/stablecoins',timeout=260)
	soup = BeautifulSoup(page.content,"html.parser")
	symbol_a = soup.find_all('a', attrs= {"class":"d-lg-none font-bold"})
	
	result = []
	for symbol in symbol_a:
		result.append(symbol.text.strip())
	return result	

def Xris():
	stable_coins = ["CETHUSDT",
"WBTCUSDT",
"STETHUSDT",
"OKBUSDT",
"CROUSDT",
"BCHAUSDT",
"MIOTAUSDT",
"CUSDCUSDT",
"BSVUSDT",
"LEOUSDT",
"AMPUSDT",
"CDAIUSDT",
"CELUSDT",
"OHMUSDT",
"HBTCUSDT",
"XDCUSDT",
"DESOUSDT",
"OMIUSDT",
"HTUSDT",
"TELUSDT",
"NEXOUSDT",
"OSMOUSDT",
"SAFEMOONUSDT",
"NXMUSDT",
"KCSUSDT",
"RENBTCUSDT",
"XSUSHIUSDT",
"CUSDTUSDT",
"LNUSDT",
"GTUSDT",
"CHSBUSDT",
"MOVRUSDT",
"GLMUSDT",
"SCRTUSDT",
"ERGUSDT",
"RPLUSDT",
"SPELLUSDT",
"DAGUSDT",
"TITANUSDT",
"HEROUSDT",
"OXYUSDT",
"LYXEUSDT",
"VXVUSDT",
"ARRRUSDT",
"WOOUSDT",
"SETHUSDT",
"XPRTUSDT",
"ANCUSDT",
"EWTUSDT",
"UBTUSDT",
"MEDUSDT",
"BCDUSDT",
"PLEXUSDT",
"ORBSUSDT",
"AKTUSDT",
"TIMEUSDT",
"ETNUSDT",
"SNTUSDT",
"MNGOUSDT",
"RGTUSDT",
"NPXSUSDT"
]


	pair = 'USDT'
	f=open('token_list.txt','r')
	list_coin=[]
	for x in f:
	    coin = x.strip()
	    coin = coin+pair
	    list_coin.append(coin.upper())
	for el in stable_coins:
	    list_coin.remove(el)
	
	period = '30m'
	date_analysis = datetime.datetime.now()

	for ticker in list_coin:
	    message = '@@@@@@@@@@@@@@@@@@@@@@@@2 ' + ticker + '@@@@@@@@@@@@@@@@@@@@@@@@@@' + '\n'
	    message = message + '\n'
	    
	    path = '/Users/mirco/Desktop/101/Binance/Bot/'+ticker+'/'+ticker+period+'.txt'
	    path_coin = '/Users/mirco/Desktop/101/Binance/Xris/'+ticker+'-'+date_analysis.strftime('%d-%m-%Y')+'.txt'
	    f = open(path,'r')
	    g= open(path_coin,'w')
	    payload = f.read()
	    closes = json.loads(payload)
	    f.close()
	    #np_closes = np.array(closes,dtype='f8')
	    np_closes = []
	    for el in closes:
	        np_closes.append(float(el))
	    closes = np_closes
	   
	    message =message + '1) one month trend ------> '
	    if np_closes[0] > np_closes[len(closes)-1]:
	        message =message + 'DOWNWARD' + '\n'
	    else:
	        message =message + 'UPWARD'     + '\n'
	    message =message + '2) first half month trend ------> '  
	    if np_closes[0] > np_closes[int(len(closes)/2)]:
	        message =message + 'DOWNWARD' + '\n'
	    else:
	        message =message + 'UPWARD'     + '\n'
	    message =message + '3) second half month trend ------> ' 
	    if np_closes[int(len(closes)/2)] > np_closes[len(closes)-1]:
	        message =message + 'DOWNWARD' + '\n'
	    else:
	        message =message + 'UPWARD'     + '\n'    
	    message =message + '4) different lowest and highest in % ------>  '
	    maxx = max(np_closes)
	    minn = min(np_closes)
	    message = message + str((maxx-minn)/minn*100)+' %' +'\n' 
	    message = message + "5)Find the % from starting point to the highest point/lowest point -------> " +  str((np_closes[0]-maxx)/maxx*100)+ ' %/ '+str((np_closes[0]-minn)/minn*100)+ ' %/ ' + '\n'
	    message = message + '6)Find the % from starting point to the highest point/lowest point -------> ' +  str((np_closes[len(closes)-1]-maxx)/maxx*100)+ ' %/ '+str((np_closes[len(closes)-1]-minn)/minn*100)+ ' %/ ' + '\n'

	    minnx = 1.05*minn
	    count = 0
	    for price in closes:
	        if price <= minnx:
	            count = count +1
	    message =message + '7) times the price drops close to lowest +o- 5% point % ------>  ' +str(count) + '\n'      

	    percentage = [1.20,1.30,1.40]
	    count = 0


	    g.write(message)
	    g.close()	