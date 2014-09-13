import time
import smtplib

SWITCH_PIN = 23
PIR_PIN = 24
DEFAULT_MIN_HRS = 4
PIR_DETECTED        =  False
SWITCH_DEPRESSED    =  True
minHrsBetweenEmails = DEFAULT_MIN_HRS
lastSend = -minHrsBetweenEmails * 3600000
box_last_opened = 0
box_last_movement = 0
# should probably  figure out how to interface 
sender = 'hackathoncmumailbox@gmail.com'
receivers = ['alexritos753@gmail.com','jocelyn@andrew.cmu.edu']
message = """From: Snail Mail Alert <from@fromdomain.com>
To: To Person <to@todomain.com>
Subject: SMTP e-mail test

This is a test e-mail message.
"""

def setup():
  pinMode(pirPin, INPUT);
  Serial.begin(9600);

def check_PIR():
    PIR_DETECTED = digital_read(PIR_PIN)
    if(PIR_DETECTED):
        box_last_movement = millis()
    
def check_switch():
    SWITCH_DEPRESSED = digital_read(SWITCH_PIN)
    if(PIR_DETECTED):
        box_last_opened = millis()    
  
def send_email():
    try:
       smtpObj = smtplib.SMTP('localhost')
       smtpObj.sendmail(sender, receivers, message)         
       print "Successfully sent email"
    except SMTPException:
        print "Error: unable to send email"
     
def loop():
	while(True):
		now = millis()
		check_PIR()
		check_switch()
		
		if(now-box_last_opened>30000):
                    if (PIR_DETECTED):
			if (now > (lastSend + minHrsBetweenEmails)):
				send_email(now)
				lastSend = now
		    
  
		sleep(500)
	

