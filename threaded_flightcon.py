# The flight control program except using threads this time so we have less code duplication
# Imports
import threading, time
import busio
from board import *
from adafruit_bus_device.i2c_device import I2CDevice
import adafruit_mpl3115a2
from adafruit_lsm6ds.ism330dhcx import ISM330DHCX
from datetime import datetime
import espeak

# Required arming altitude - we need to get this high to allow apogee sensing to work
required_alt = 1000
# Pressure is in hPa
sea_pressure = 102.3

#Final variables to transmit to ground
max_x_accel = 0
max_y_accel = 0
max_z_accel = 0
accel_x_values = []
accel_y_values = []
accel_z_values = []
# Altitude
max_alt = 0
start_alt = 0
descent_rate = 10
alt_values = []
flight_finished = false
#Temperature
max_temp = 0
temp_values = []

update_interval = 0.5 #in seconds

def xmit_string(instring):
    transmitter = espeak.ESpeak()
    transmitter.say(instring)
    return

def accel_monitor_thread():
    global max_x_accel, max_y_accel, max_z_accel
    global accel_x_values, accel_y_values, accel_z_values
    global flight_finished
    while(not flight_finished):
        # Do accel stuff on a loop
        x, y, z = accelerometer.acceleration
        accel_x_values.append(x)
        accel_y_values.append(y)
        accel_z_values.append(z)
        if(x > max_x_accel):
            max_x_accel = x
        if(y > max_y_accel):
            max_y_accel = y
        if(z > max_z_accel):
            max_z_accel = z
        time.sleep(update_interval)

def alt_monitor_thread():
    global max_alt, start_alt, flight_finished
    start_alt = altimeter.altitiude
    required_alt = start_alt + required_alt
    max_alt = start_alt
    apogee = False
    curr_alt = 0
    while(not apogee):
        curr_alt = altimeter.altitude
        if(curr_alt > max_alt):
            max_alt = curr_alt
        else: 
            if(curr_alt > required_alt):
                apogee = True
            else:
                continue
        alt_values.append(curr_alt)
        time.sleep(update_interval)
    
    # Post-apogee loop - expecting descent rate of at least descent_rate
    timeout = 0
    while(timeout < 3):
        if(curr_alt - descent_rate > altimeter.altitude):
            curr_alt = altimeter.altitude
            alt_values.append(curr_alt)
        else:
            timeout += 1
        time.sleep(update_interval)

def temp_monitor_thread():
    global max_temp, temp_values