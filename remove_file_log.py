import os 
import datetime

number_bots = 4
not_remove = datetime.datetime.now().strftime('%d-%m-%Y')+'.txt'

main_path = '/home/pi/Desktop/Binance/Bot/bot'

files ={}

for i in range(1,number_bots+1):
	path =main_path+str(i)+'/log/'
	files[str(i)] = []
	for (dirpath,dirnames,filenames) in os.walk(path):

		files[str(i)].extend(filenames)

for bot in  files.keys():
	path =main_path+bot+'/log/'	
	for file in files[bot]:	
		if(file != not_remove):
			os.remove(path+file)
			print(file,'DELETED')
		
	
	