import Utilities.utilitiesFunction as utilities
import bot



if __name__=="__main__":

	print("Choices:")
	print("1. Bot.")
	print("2. Test Bot.")
	print("3. Updating Database.")
	print("4. Retrieve a new list of coins.")
	print("5. Plotting")

	choice = int(input())

	match choice:
		case 1:
			bot.run()
		case 2:
			pass	
		case 3:
			print("Choices:")
			print("1. Update all the database")
			print("2. Specify coins and intervals")
			choice = int(input())
			match choice:
				case 1:
					utilities.updateDatabase()
				case 2:
					print("Write the list of coin/pair separate by ,")
					
					list_tickers_input  = input()
					list_tickers = list_tickers_input.split(",")
					list_tickers = [(i.strip()).upper()for i in list_tickers ]
					
					print("Write the intervals separate by ,. m for minute, h for hour , 1 for day, w for week, M for month ")
					print("You can choice among 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 12h, 1d, 1w, 1M")
					
					interval_input = input()
					interval = interval_input.split(",")
					interval = [i.strip() for i in interval ]
					
					utilities.updateDatabase(list_tickers, interval )
		case 4 :
			print("Write the list of coin/pair separate by ,")
					
			list_tickers_input  = input()
			list_tickers = list_tickers_input.split(",")
			list_tickers = [(i.strip()).upper() for i in list_tickers ]
			print("How many years do you want to retrieve?")
			
			year = int(input())
			
			print("Do you want retrieve specific intervals? [y/n]")

			yes_not = input()
			if yes_not == 'y':
				print("Write the intervals separate by ,. m for minute, h for hour , 1 for day, w for week, M for month ")
				print("You can choice among 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 12h, 1d, 1w, 1M")
					
				interval_input = input()
				interval = interval_input.split(",")
				interval = [i.strip() for i in interval ]

				utilities.retrieveDataYear(list_tickers,year,interval)

			else:
				utilities.retrieveDataYear(list_tickers,year)

		case 5:
			pass

		case other:
			print("Not a Choice")		



