import time
import RPi.GPIO as GPIO
from qhue import Bridge
import random
from phue import Bridge

GPIO.setmode(GPIO.BOARD)
pin = 18
GPIO.setup(pin, GPIO.IN)

b = Bridge("192.168.1.146","nmvFoVSeJELdmDahQNveYNgFueNvW4WG15HeN5a7")
groups = b.groups

while True:
    if GPIO.input(pin) == GPIO.LOW:
        i = 3
        for l in range(1, i+1):
            print "alerting!"
            b.groups[0].action(alert="select")
            time.sleep(1)

        time.sleep(3)

