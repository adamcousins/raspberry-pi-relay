#!/usr/bin/env python

# This is my first script.

print "Hello Python"

import time

try:
    import RPi.GPIO as GPIO

    #Set PIN Numbering mode (more info here: https://raspberrypi.stackexchange.com/questions/12966/what-is-the-difference-between-board-and-bcm-for-gpio-pin-numbering)
    GPIO.setmode(GPIO.BCM)

except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")

#Set channel 21 as an output
GPIO.setup(21, GPIO.OUT, initial=GPIO.LOW)

GPIO.output(21, not GPIO.input(21))

# when your code ends, the last line before the program exits would be...  
time.sleep(5)

GPIO.cleanup() 

GPIO.RPI_INFO 
