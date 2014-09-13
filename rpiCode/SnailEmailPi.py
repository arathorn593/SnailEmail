import RPi.GPIO as GPIO, time

SWITCH_PIN = 23
PIR_PIN = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN)
GPIO.setup(SWITCH_PIN, GPIO.IN)

def millis():
	return int(round(time.time()*1000))

def check_PIR():
   
def check_switch():
 
def send_email():
     
def loop():
	
loop()
