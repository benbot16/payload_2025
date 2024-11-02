#!/usr/bin/python
# Script for shutting down the raspberry Pi using the Adafruit PowerBoost 1000c.

import RPi.GPIO as GPIO
import time
import os

pwrpin = 4

GPIO.setmode(GPIO.BCM)
GPIO.setup(pwrpin, GPIO.IN)

while True:

# Shutdown function
  low = not(GPIO.input(pwrpin))
  if low:
    os.system('shutdown -h now')
  time.sleep(1)