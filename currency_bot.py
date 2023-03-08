import websocket,json,pprint
import time
from  utilities import getPrecision
import utilities
from  Constant import *
import Constant

def computeProfit():
	global profit_map
	budget = 200.0
	fee = (1-0.1/100)
	criteria = price[pairing+currency]/price['USDT'+currency] > price[pairing+'USDT']
	if criteria:
		profit = fee**3*(price['USDT'+currency]*price[pairing+'USDT'])/price[pairing+currency]
	else:
		profit = fee**3*price[pairing+currency]/(price['USDT'+currency]*price[pairing+'USDT'])
	if profit > profit_map[currency]:
		try:
			pprint.pprint(price)
			pprint.pprint(currency)
			pprint.pprint(profit)
			if criteria:
				order_sell = budget*price['USDT'+currency]*fee
				
				order_buy  = getPrecision(order_sell*fee/price[pairing+currency],5)
			
				quantity_quote = order_buy*price[pairing+'USDT']*fee 
				
			else:	
				#order_buy = client.order_market_buy( symbol=pairing+'USDT' , quantity= utilities.getPrecision(quantity_quote,STEP_QUOTE))
				order_buy_executedQty = getPrecision(budget*fee/price[pairing+'USDT'],5)
			
				#order_sell  = client.order_market_sell( symbol=pairing+currency , quantity= order_buy['executedQty'])
				order_sell_cummulativeQuoteQty = int(order_buy_executedQty*price[pairing+currency]*fee)
			
				#order_buy = client.order_market_sell( symbol='USDT'+currency , quantity= order_sell['cummulativeQuoteQty'])
				#order_buy[]quantity_quote
				quantity_quote = (order_sell_cummulativeQuoteQty/price['USDT'+currency])*fee
				
			utilities.log('--------------------------------','')
			utilities.log(currency,'')
			utilities.log(str(profit),'')
			utilities.log(str(quantity_quote- budget),'')
			utilities.log('--------------------------------','')
			if quantity_quote - budget > 0: 
				time.sleep(30)
			else:
				profit_map[currency] =	profit
		except Exception as e:
			print(e) 	
def websocket_bot():
	ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message, 
											on_error = on_error)
	ws.run_forever()
def on_open(ws):
    print('opened connection')
    utilities.log('opened connection ' + currency+'  ' + pairing ,OUTCOME_OK)

def on_close(ws, close_status_code, close_msg):
	print('closed connection')
	utilities.log('closed connection '+ str(close_status_code) + ' '+ str(close_msg) ,OUTCOME_OK)
	ws.close()
	time.sleep(60)
	websocket_bot()
def on_error(ws,error):
	utilities.log('WebSocket ERROR ' + str(error) ,OUTCOME_KO)

def on_message(ws,message):
	global price
	json_message= json.loads(message)
	#pprint.pprint(json_message)
	candle = json_message['data']['k']
	
	price[candle['s']] = float(candle['c'])
	
	computeProfit()





if __name__ == "__main__":
	price = {}
	pairing = 'ETH'
	profit_map = {'NGN':1.00,'RUB':1.00,'UAH':1.00}

	print('NGN or UAH or RUB')
	currency=input().upper()
	streams = [pairing+'USDT',pairing+currency,'USDT'+currency]
	request_message = ''
	for stream in streams:
		request_message = request_message + stream.lower()+'@kline_1m/'
		price[stream] = 0.0
	
	SOCKET = "wss://stream.binance.com:9443/stream?streams="+request_message[0:len(request_message)-1]
	websocket_bot()
