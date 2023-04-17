import ssl
import smtplib,ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text  import MIMEText
import datetime
import traceback
import time 
import asyncio
import utilities
from email.mime.base import MIMEBase
from email import encoders
import config

# Send the wrap-up email with log file  attached 

def sendNotification(subject,text):

	today = datetime.datetime.now()
	yesterday  = today - datetime.timedelta(days=1)

	#https://docs.python.org/3/library/email.examples.html
	smtp_server = "smtp.mail.yahoo.com"
	

	sender_email = config.SENDER_EMAIL
	password = config.PASSWORD
	
	receiver = config.RECEIVER_EMAIL
	port = 587
	
	
	#context = ssl.create_default_context()

	#Setting up the email
	msg = MIMEMultipart('Empty')
	msg['From'] = sender_email
	msg['To'] = receiver
	msg['Subject'] = subject
	body = text
	msg.attach(MIMEText(body,'plain'))          
	#server = smtplib.SMTP_SSL(smtp_server, port, context=context)

	# Attach the log file
	part = MIMEBase('application', "octet-stream")
	part.set_payload(open("log/"+yesterday.strftime('%d-%m-%Y') +".txt", "rb").read())
	encoders.encode_base64(part)
    
	part.add_header('Content-Disposition', 'attachment; filename="log.txt"')

	msg.attach(part) 



	try:

		mail = smtplib.SMTP(smtp_server,port)
		debuglevel = True
		mail.set_debuglevel(debuglevel)
		mail.ehlo()
		if mail.has_extn('STARTTLS'):
			mail.starttls()
			mail.ehlo()
	
		mail.login(sender_email,password)
	
		mail.sendmail(sender_email,receiver,msg.as_string())
		
		print('@@@@@@@@@@@@@@@@@@@@the email has sent ')
		mail.quit()

	except Exception as e:
		#timeError = datetime.datetime.now()
		#sendNotification('EMAIL NOT SENT - '+ str(timeError), str(traceback.print_exc()))
		#time.sleep(10)
		print(traceback.print_exc())
		return False
		
	
		
	return True

		
