# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import RPi.GPIO as GPIO
import time
import os

SWITCH_PIN = 23
PIR_PIN = 24
BOX_NUM = 5189
EMAIL_ADDR = "rpaetz@andrew.cmu.edu"
EMAIL_SUBJECT = "You Have (Snail)Mail!"

def setupGPIO(pirPin, switchPin):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pirPin, GPIO.IN)
    GPIO.setup(switchPin, GPIO.IN)

#GPIO input wrapped for more clarity
def movement(pirPin):
    if(GPIO.input(pirPin) == 1):
        return True
    else:
        return False

def doorOpen(doorPin):
    #print "checking if door open...",
    if(GPIO.input(doorPin) == 1):
        #print "door closed"
        return False
    else:
        #print "door open"
        return True

def craftMessage(boxNum):
    message = """Hello owner of mailbox %s
        You have new mail!!! Congratulations!!!
    """
    message = message % (str(boxNum))
    return message

def sendEmail(message, reciever, subject):
    emailCommand = ("echo \"" + message + "\" | mail -s \"" + 
               subject + "\" " + reciever)
    #os.system(emailCommand)
    print "send Email"

def queEmail(message, reciever, subject, doorPin):
    print "QueEmail"
    delay = 30 #in seconds
    for x in xrange(delay):
        print "Sending email in", delay - x, "seconds"
        if(doorOpen(doorPin)):
            return False
        time.sleep(1)
    sendEmail(message, reciever, subject)
    return True

def loop():
    #the checkNewMail and emailSent variables could be implemented better
    #see the case when both are true. if sentEmail = true, checkNewMail should be False
    checkNewMail = False
    emailSent = False 
    while True:
        if(checkNewMail):
            if(doorOpen(SWITCH_PIN)):
                emailSent = False
                checkNewMail = False
            elif(not emailSent and movement(PIR_PIN)):
                message = craftMessage(BOX_NUM)
                emailSent = queEmail(message, EMAIL_ADDR, EMAIL_SUBJECT, SWITCH_PIN)
        elif(not doorOpen(SWITCH_PIN) and not movement(PIR_PIN)):
            checkNewMail = True
        time.sleep(1)
        print "checkNewMail =", checkNewMail, "emailSent =", emailSent

setupGPIO(PIR_PIN, SWITCH_PIN)
loop()
