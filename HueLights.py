#Code for the hue lights to be mainpulated with the temperature sensor in the raspberry pi

import requests
import json
from random import randint
import time
import RPi.GPIO as GPIO

import os
import glob

os.system("modprobe w1-gpio")
os.system("modprobe w1-therm")

GPIO.setmode(GPIO.BCM)
pin1 = 18
pin2 = 4
GPIO.setup(pin1, GPIO.IN)
GPIO.setup(pin2, GPIO.IN)

url = "http://192.168.1.146/api/vXhBvbpEXm8nuEYm79tmNsCrRpAnhac1-EFaDXYp/groups/0/action"

#data_on = {"on": True, "sat":254, "bri":254, "hue":randint(1, 65535)}
#data_off = {"on": False}

base_dir = "/sys/bus/w1/devices/"
device_folder = glob.glob(base_dir + "28*")[0]
device_file = device_folder + "/w1_slave"

def read_temp_raw():
    f = open(device_file, "r")
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != "YES":
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find("t=")
    if equals_pos != -1:
        temp_string = lines[1][equals_pos + 2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32
        return temp_c, temp_f

temp_c_threshold = 27

data = {}
data["brightness"] = 254 * 0.5
data["saturation"] = 254 * 1
data["hue"] = 40000
r = requests.put(url, json.dumps(data), timeout = 6)
time.sleep(1)

while (1==1):
    data = {}
    if GPIO.input(pin1) == GPIO.LOW:
        data["on"] = True
    elif GPIO.input(pin1) == GPIO.HIGH:
        data["on"] = True

    temp_c, temp_f = read_temp()
    data["brightness"] = 254 * 0.5
    data["saturation"] = 254 * 1

    
    if temp_c < temp_c_threshold:
        data["hue"] = 45000
    elif temp_c >= temp_c_threshold:
        data["hue"] = 1000
    else:
        data["hue"] = 20000
        data["brightness"] = 254 * 1

    data["hue"] = int(65535 * (1- (temp_c - 25) / 15))
    if data["hue"] <  0:
        data["hue"] = 0
    elif data["hue"] > 65535:
        data["hue"] = 65535
        
    
    print(temp_c)
    print(data)
    r = requests.put(url, json.dumps(data), timeout = 6)
    time.sleep(0.4)
