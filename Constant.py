#----------------------------- bot Constant  --------------------------------- 
# We can run different bot simultaneously
bot_number = 1

#-----------------------------Profit Rate configuration------------------------------ 

EARNING_MAP = {'big': 1.10,'short':1.05}
EARNING = EARNING_MAP['short']
TOTAL_EARNING = 1.55

#-------------------------------Balance configuration--------------------------
# Starting FIAT Balance (STARTING_QUOTE) or Crypto Balance (STARTING_BASE)
STARTING_QUOTE = 100.00
STARTING_BASE  = 0.0
MINIMUM_AMOUNT = 0.0  # Force to BUY and SELL an amount of trading quantity always increasing  

# you must change it if STARTING_QUOTE == 0
STARTING_TRADE_QUANTITY_QUOTE = STARTING_QUOTE
PRICE_TO_SELL = 0.0
ORDER_ID = ''

#----------------------Price/Trading balance  sensibility for the orders on Binance------------------------
STEP_BASE = 0
TICK_SIZE = 0.0
STEP_QUOTE= 8

#------------------------------Trade Symbol Configuration---------------------------------------------

TRADE_SYMBOL = 'SOLEUR'
RSI_LENGTH = 14
PERIOD = '3m'           #Kindle stick period

if STARTING_BASE == 0.0:
	IN_POSITION= True
else:
	IN_POSITION= False

# --------------------------------------------Debug constant------------------------------------- 

OUTCOME_OK = 'OK'
OUTCOME_KO = '----------KO-------------- '

# ---------------------------------------Retrieving/Utilities/Plotting Configuration-----------------------------------
PATH = 'PATH to a folder that contains specific folder names: Data, log, Photo, Analysis '
INTERVAL = ['1m','3m','5m','15m','30m']
INTERVAL2 = ['1h','2h','4h','6h','12h','1d']
RSI_PERIOD = [6,12,14,24]
EMA_LIST = list(['ema_200','ema_100','ema_50','ema_25','ema_10'])
EMA_LIST_SKIP = list(['ema_25','ema_10'])
NUMBER_OF_MINIMUM = 55



