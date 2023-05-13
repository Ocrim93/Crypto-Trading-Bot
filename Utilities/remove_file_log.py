'''
In case you have more bots which run simultaneously. 

It is a script to prompt erasing of the past log files

'''


import os 
import datetime

# Number of bots 
number_bots = 4

# Not remove the log file of today
not_remove = datetime.datetime.now().strftime('%d-%m-%Y')+'.txt'

main_path = 'PATH TO GENERAL BOT FODLER /bot'

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
		
	
	