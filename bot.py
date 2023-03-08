import websocket,json,pprint
import numpy as np
import  time
import datetime
from Constant import *
import utilities,utilities_bot
import traceback,sys
from websocket._exceptions import *
import Constant



def daily_initialization(ws):
	global price, summary_book,change_day_alert
	utilities.send_summary_email(summary_book)
	change_day_alert = True
	summary_book = []
	for key in price.keys():
		price[key] = price[key][len(price[key])-EMA_PERIOD:len(price[key])]

	try:
		ws.close()
		time.sleep(120+bot_number)
		websocket_bot()

	except Exception as e:
		utilities.log(str(e), OUTCOME_KO)
		utilities.log('Detail : \n',str(traceback.print_exc()))



def websocket_bot():
	try:
		#websocket.enableTrace(True)
		ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message, 
											on_error = on_error, on_pong = on_pong,on_ping=on_ping)
		ws.run_forever()
		

	except WebSocketTimeoutException as WebErrorTimeout :

		utilities.log(str(WebErrorTimeout), OUTCOME_KO)
		exc_type, exc_obj, exc_tb = sys.exc_info()
		utilities.log('Detail : \n',str(traceback.extract_tb(exc_tb)))
		ws.close(status=websocket.STATUS_PROTOCOL_ERROR)
		
		time.sleep(30)
		websocket_bot()		

	except WebSocketException as WebError :

		utilities.log(str(WebError), OUTCOME_KO)
		exc_type, exc_obj, exc_tb = sys.exc_info()
		utilities.log('Detail : \n',str(traceback.extract_tb(exc_tb)))
		ws.close()
		
		time.sleep(540)
		websocket_bot()	

	except WebSocketConnectionClosedException as closeError:

		utilities.log(str(closeError), OUTCOME_KO)
		exc_type, exc_obj, exc_tb = sys.exc_info()
		utilities.log('Detail : \n',str(traceback.extract_tb(exc_tb)))
		ws.close()
		time.sleep(540)
		websocket_bot()	

	except WebSocketBadStatusException as badStatus:

		utilities.log(str(badStatus), OUTCOME_KO)
		exc_type, exc_obj, exc_tb = sys.exc_info()
		utilities.log('Detail : \n',str(traceback.extract_tb(exc_tb)))
		ws.close()
		time.sleep(540)
		websocket_bot()

	except KeyboardInterrupt as interruption:
		ws.close()

	except Exception as e:
		utilities.log(str(e), OUTCOME_KO)
		exc_type, exc_obj, exc_tb = sys.exc_info()
		utilities.log('Detail : \n',str(traceback.extract_tb(exc_tb)))

def on_open(ws):
    print('opened connection')
    utilities.log('opened connection',OUTCOME_OK)

def on_close(ws, close_status_code, close_msg):
	print('closed connection')
	utilities.log('closed connection '+ str(close_status_code) + ' '+ str(close_msg) ,OUTCOME_OK)

def on_ping(ws, message):
    utilities.log('PING RECEIVED ',OUTCOME_OK)

def on_pong(ws, message):
	utilities.log('PONG RECEIVED ',OUTCOME_OK)
    
def on_error(ws,error):
	utilities.log('WebSocket ERROR ' + str(error) ,OUTCOME_KO)
	if(error == '[Errno 110] Connection timed out'):
		ws.close()
		time.sleep(180)
		websocket_bot()


def on_message(ws,message):
	global price, orderId,in_position,price_to_sell,change_day_alert,change_day,TRADE_QUANTITY_QUOTE,TRADE_QUANTITY_BASE,summary_book
	current_price = {'low': 0.0, 'high':0.0,'close':0.0}
	
	try:
		json_message= json.loads(message)
		pprint.pprint(json_message)

		candle = json_message['k']

		is_candle_closed = candle['x']

		current_price['close'] = float(candle['c'])
		current_price['low'] = float(candle['l'])
		current_price['high'] = float(candle['h'])
		current_price['volume'] = float(candle['v'])

		close_Time = candle['T']


		close_date = datetime.datetime.fromtimestamp(close_Time/1000)
		if change_day_alert :
			change_day = close_date.replace(minute=59,hour=23,second=59,microsecond=999999)
			utilities.log('set change_day', str(change_day))
			change_day_alert = False
		if( close_date > change_day ):
			daily_initialization(ws)
		
		if (not in_position and current_price['close'] >= price_to_sell):
			time.sleep(3)
			order = utilities_bot.checkExecutionOrder(orderId)
			if order != {} :
				in_position = True
				TRADE_QUANTITY_QUOTE = float(order['cummulativeQuoteQty']) + TRADE_QUANTITY_QUOTE
				TRADE_QUANTITY_BASE  = TRADE_QUANTITY_BASE - float(order['executedQty'])
				summary_book.append(utilities_bot.formatting_page(order,TRADE_QUANTITY_BASE,TRADE_QUANTITY_QUOTE))
			else:
				utilities.log('LIMIT ORDER NOT FILLED', OUTCOME_KO)

		if is_candle_closed:
			for key in price.keys():
				price[key] = np.append(price[key],current_price[key])

			
			bot_rsi_output = utilities_bot.bot_rsi(price, in_position,orderId,price_to_sell,TRADE_QUANTITY_QUOTE,TRADE_QUANTITY_BASE,summary_book)
			if in_position != bot_rsi_output['in_position']:
				in_position = bot_rsi_output['in_position']
				TRADE_QUANTITY_QUOTE  = bot_rsi_output['TRADE_QUANTITY_QUOTE']
				TRADE_QUANTITY_BASE  = bot_rsi_output['TRADE_QUANTITY_BASE']
				summary_book  = bot_rsi_output['summary_book']
				price_to_sell = bot_rsi_output['price_to_sell']
				orderId = bot_rsi_output['orderId_to_sell']
				
			if (TRADE_QUANTITY_QUOTE > STARTING_TRADE_QUANTITY_QUOTE*TOTAL_EARNING):
				ws.close()
				utilities.send_summary_email(summary_book)
			
	except Exception as e:						
		
		utilities.log(str(e), OUTCOME_KO)
		exc_type, exc_obj, exc_tb = sys.exc_info()
		utilities.log('Detail : \n',str(traceback.extract_tb(exc_tb)))


if __name__ == "__main__":

	TRADE_QUANTITY_BASE = STARTING_BASE
	TRADE_QUANTITY_QUOTE = STARTING_QUOTE
	
	price_to_sell = PRICE_TO_SELL

	orderId = ORDER_ID

	in_position = IN_POSITION
	change_day_alert = True
	
	utilities.setTICKandSTEPvalue()

	symbol  = TRADE_SYMBOL.lower()
	stream = symbol+'@kline_'+PERIOD

	SOCKET = "wss://stream.binance.com:9443/ws/"+ stream
	summary_book = []

	price = utilities.retrieveData([TRADE_SYMBOL],interval=[PERIOD],howLong=15)
	websocket_bot()
