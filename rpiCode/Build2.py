import subprocess
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
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN)
GPIO.setup(SWITCH_PIN, GPIO.IN)
user = ""

def millis():
	return int(round(time.time()*1000)) 
def bash_command(cmd):
	subprocess.Popen(cmd,shell=True,executable ='/bin/bash')

def check_PIR():
    PIR_DETECTED = GPIO.input(PIR_PIN)
    if(PIR_DETECTED!=0):
	print "movement Detected"
	box_last_movement = millis()
    
def check_switch():
    SWITCH_DEPRESSED = GPIO.input(SWITCH_PIN)
    if(SWITCH_DEPRESSED==0):
	box_last_opened = millis()    
	print "box opened"
def get_user():
	#Stubbed
	return "7863529674@vtext.com"
  
def send_email():
	print "Should have emailed"
	#try:
	#	smtpObj = smtplib.SMTP('localhost')
       	#	smtpObj.sendmail(sender, receivers, message)         
       	#	print "Successfully sent email"
    	#except SMTPException:
	#	print "Error: unable to send email"
	bash_command('mail -s "You have recieved mail!" < /dev/null "%s"',user)
     
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
                    if (PIR_DETECTED!=0):
			if (now > (lastSend + minHrsBetweenEmails)):
				send_email(now)
				lastSend = now
		    
  
		time.sleep(0.5)
user=get_user()
loop()

