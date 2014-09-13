import smtplib
import RPi.GPIO as GPIO, time

SWITCH_PIN = 23
PIR_PIN = 24
DEFAULT_MIN_HRS = 4
PIR_DETECTED        =  0
SWITCH_DEPRESSED    =  0
minHrsBetweenEmails = DEFAULT_MIN_HRS
lastSend = -minHrsBetweenEmails * 3600000
box_last_opened = 0
box_last_movement = 0
# should probably  figure out how to interface 
sender = 'hackathoncmumailbox@gmail.com'
receivers = ['alexritos753@gmail.com','jocelynh@andrew.cmu.edu']
message = """From: Snail Mail Alert <from@fromdomain.com>
To: To Person <to@todomain.com>
Subject: SMTP e-mail test

This is a test e-mail message.

"""
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN)
GPIO.setup(SWITCH_PIN, GPIO.IN)

#
#def setup():
#  pinMode(pirPin, INPUT);
#  Serial.begin(9600);
def millis():
	return int(round(time.time()*1000))

def check_PIR():
    PIR_DETECTED = GPIO.input(PIR_PIN)
    if(PIR_DETECTED==1):
	print "movement Detected"
	box_last_movement = millis()
    
def check_switch():
    SWITCH_DEPRESSED = GPIO.input(SWITCH_PIN)
    if(SWITCH_DEPRESSED==0):
	print "box opened"
	box_last_opened = millis()    
  
def send_email():
	print "Should have emailed"
	try:
		smtpObj = smtplib.SMTP('localhost')
       		smtpObj.sendmail(sender, receivers, message)         
       		print "Successfully sent email"
    	except SMTPException:
        	print "Error: unable to send email"
     
def loop():
	while(True):
		now = millis()
		print "it is now ",now
		check_PIR()
		print box_last_movement
		check_switch()
		print box_last_opened
		switchVal = GPIO.input(SWITCH_PIN)
		pirVal = GPIO.input(PIR_PIN)
		print "switch = ", switchVal,"| PIR = ", pirVal	
		if(now-box_last_opened>30000):
                    if (PIR_DETECTED):
			if (now > (lastSend + minHrsBetweenEmails)):
				send_email(now)
				lastSend = now
		    
  
		time.sleep(0.5)
	
loop()
