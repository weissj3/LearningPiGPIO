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

while(1):
    if CheckQuit(): break;
    GPIO.output(17, GPIO.HIGH);
    print "HIGH"
    time.sleep(2);
    
    GPIO.output(17, GPIO.LOW);
    print "LOW"
    time.sleep(2);
    
GPIO.cleanup();
