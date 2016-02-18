import RPi.GPIO as GPIO
import sys, select, os
import time

def CheckQuit():
    if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
        line = raw_input()
        return 1;
    return 0;

GPIO.setmode(GPIO.BCM);

GPIO.setup(17, GPIO.OUT);
GPIO.setup(18, GPIO.IN);

LEDState = 0;
PastPushState = 0;
GPIO.output(17, GPIO.LOW);

while(1):
    if CheckQuit(): break;
    if GPIO.input(18) and not PastPushState:
        print "Push"
        if not LEDState:
            GPIO.output(17, GPIO.HIGH);
            LEDState = 1
            print "HIGH"
        else:
            GPIO.output(17, GPIO.LOW);
            LEDState = 0
            print "LOW"
            
    PastPushState = GPIO.input(18)
    time.sleep(.1);
    
GPIO.cleanup();
