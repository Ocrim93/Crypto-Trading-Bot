#----------- bot constants 
bot_number = 1

EARNING_MAP = {'big': 1.10,'short':1.05}
EARNING = EARNING_MAP['short']
TOTAL_EARNING = 1.55

STARTING_QUOTE = 100.00
STARTING_BASE  = 0.0
MINIMUM_AMOUNT = 0.0

# you must change it if STARTING_QUOTE = 0
STARTING_TRADE_QUANTITY_QUOTE = STARTING_QUOTE
PRICE_TO_SELL = 0.0
ORDER_ID = ''

STEP_BASE = 0
TICK_SIZE = 0.0
STEP_QUOTE= 8

TRADE_SYMBOL = 'SOLEUR'
RSI_LENGTH = 14
PERIOD = '3m'

if STARTING_BASE == 0.0:
	IN_POSITION= True
else:
	IN_POSITION= False

# log constants 

OUTCOME_OK = 'OK'
OUTCOME_KO = '----------KO-------------- '

# retrieving/utilities/plotting constant 
PATH = '/Users/mirco/Desktop/101/Binance/Bot/'
INTERVAL = ['1m','3m','5m','15m','30m']
RSI_PERIOD = [6,12,14,24]
EMA_LIST = list(['ema_200','ema_100','ema_50','ema_25','ema_10'])
EMA_LIST_SKIP = list(['ema_25','ema_10'])



