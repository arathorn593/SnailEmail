# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import RPi.GPIO as GPIO, time

PIR_PIN = 24
SWITCH_PIN = 23

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN)
GPIO.setup(SWITCH_PIN, GPIO.IN)

while True:
    switchVal = GPIO.input(SWITCH_PIN)
    pirVal = GPIO.input(PIR_PIN)
    print "switch =", switchVal, "| PIR =", pirVal
    time.sleep(1)
