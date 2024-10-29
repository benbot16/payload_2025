# Imports
import time
import busio
from board import *
from adafruit_bus_device.i2c_device import I2CDevice
import adafruit_mpl3115a2

required_alt = 500 

def preflight_check(altimeter, ground_alt):
    if((altimeter.altitude - ground_alt) > required_alt):
        return True
    return False



# Start main
armed = False
# Pressure is in pascals, 1 kPa = 1000 Pa
sea_pressure = 103040

# Main Func
if __name__ == "__main__":
    #init devices
    accelerometerid = 0x6a
    altimeterid = 0x60
    i2c = busio.I2C(SCL, SDA)
    altimeter = adafruit_mpl3115a2.MPL3115A2(i2c, address=altimeterid)
    altimeter.sealevel_pressure = sea_pressure
    accelerometer = I2CDevice(i2c, accelrometerid)

    #Get original pressure/temp/alt
    init_pressure = altimeter.pressure
    init_temp = sensor.temperature
    init_alt = sensor.altitude


    while not preflight_check(altimeter, ground_alt):
            time.sleep(1)
        continue
    armed = True
    print("Arming triggered")
   
    # Continuously poll max_alt until we hit apogee and start coming down again
    # Starts at our initial ground altitude
    max_alt = init_alt
    while altimeter.altitude > max_alt:
        max_alt = altimeter.altitude
        time.sleep(0.2)

    # Do apogee-based stuff

    # Wait for the rocket to land, then collect ground data


    # Transmit ground data back to the flight station

    
    # Save data to a file
