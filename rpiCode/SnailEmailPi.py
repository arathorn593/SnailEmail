# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import RPi.GPIO as GPIO
import time
import os

SWITCH_PIN = 23
PIR_PIN = 24
BOX_NUM = 5189
EMAIL_ADDR = "rpaetz@andrew.cmu.edu"
EMAIL_SUBJECT = "You Have (Snail)Mail!"

GPIO.setmode(GPIO.BCM)

class SMCBox:
    pirPin = None
    doorPin = None
    boxNum = None
    emailAddr = None
    emailSent = False
    checkForMail = False
    emailSubject = "You Have (Snail)Mail!"

    def __init__(self, pirPinTemp, doorPinTemp, boxNumTemp, emailAddrTemp):
        print "initialze box", boxNumTemp
        self.pirPin = pirPinTemp
        self.doorPin = doorPinTemp
        self.boxNum = boxNumTemp
        self.emailAddr = emailAddrTemp
        GPIO.setup(self.pirPin, GPIO.IN)
        GPIO.setup(self.doorPin, GPIO.IN)

    #GPIO input wrapped for more clarity
    def movement(self):
        if(GPIO.input(self.pirPin) == 1):
            return True
        else:
            return False

    
    def doorOpen(self):
        #print "checking if door open...",
        if(GPIO.input(self.doorPin) == 1):
            #print "door closed"
            return False
        else:
            #print "door open"
            return True

    def runCheck(self):
        if(not self.emailSent):
            if(self.checkForMail):
                if(self.doorOpen()):
                    self.checkForMail = False
                elif(self.movement()):
                    self.sendEmail()
            elif(not self.doorOpen() and not self.movement()):
                self.checkForMail = True
        else:
            if(self.doorOpen()):
                self.emailSent = False
        print "checkForMail =", str(self.checkForMail), " emailSent =", str(self.emailSent)

    def sendEmail(self):       
        message = """Hello owner of mailbox %s
            You have new mail!!! Congratulations!!!
        """
        message = message % (str(self.boxNum))
        emailCommand = ("echo \"" + message + "\" | mail -s \"" + 
                   self.emailSubject + "\" " + self.emailAddr)
        os.system(emailCommand)
        print "send Email"
        self.emailSent = True

'''
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
'''

def loop():
    #the checkNewMail and emailSent variables could be implemented better
    #see the case when both are true. if sentEmail = true, 
    #checkNewMail should be False
    '''
    checkNewMail = False
    emailSent = False 
    while True:
        if(checkNewMail):
            if(doorOpen(SWITCH_PIN)):
                emailSent = False
                checkNewMail = False
            elif(not emailSent and movement(PIR_PIN)):
                message = craftMessage(BOX_NUM)
                emailSent = sendEmail(message, EMAIL_ADDR, EMAIL_SUBJECT)
        elif(not doorOpen(SWITCH_PIN) and not movement(PIR_PIN)):
            checkNewMail = True
        time.sleep(1)
        print "checkNewMail =", checkNewMail, "emailSent =", emailSent
    '''
    while True:
        for box in registeredBoxes:
            box.runCheck()
        time.sleep(0.5)


myBox = SMCBox(PIR_PIN, SWITCH_PIN, BOX_NUM, EMAIL_ADDR)
registeredBoxes = [myBox]
loop()
