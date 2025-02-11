# Imports
import time
import busio
from board import *
from adafruit_bus_device.i2c_device import I2CDevice
import adafruit_mpl3115a2
from adafruit_lsm6ds.ism330dhcx import ISM330DHCX

required_alt = 500 

def preflight_check(altimeter, ground_alt):
    if((altimeter.altitude - ground_alt) > required_alt):
        return True
    return False

# Start main
armed = False
# Pressure is in pascals, 1 kPa = 1000 Pa
sea_pressure = 101016
# Var defines
max_alt = 0
ALT_DELTA_LANDED = 5

# Main Func
if __name__ == "__main__":
    #init devices
    accelerometerid = 0x6a
    altimeterid = 0x60
    i2c = busio.I2C(SCL, SDA)
    altimeter = adafruit_mpl3115a2.MPL3115A2(i2c, address=altimeterid)
    altimeter.sealevel_pressure = sea_pressure
    accelerometer = ISM330DHCX(i2c, address=accelerometerid)

    #Get original pressure/temp/alt
    init_pressure = altimeter.pressure
    print("Init pressure: " + init_pressure)
    init_temp = altimeter.temperature
    print("Init temperature: " + init_temp)
    init_alt = altimeter.altitude
    print("Init altitude: " + init_alt)


    # Check every second to see if we've started flying
    while not preflight_check(altimeter, init_alt):
        time.sleep(1)

    armed = True
    print("Arming triggered")
   
    # Continuously poll max_alt until we hit apogee and start coming down again
    # Starts at our initial ground altitude
    max_alt = init_alt
    while altimeter.altitude > max_alt:
        max_alt = altimeter.altitude
        time.sleep(0.2)

    # Do apogee-based stuff
    print("Apogee: " + max_alt)

    # Wait for the rocket to land, then collect ground data
    current_alt = altimeter.altitude - ALT_DELTA_LANDED
    while(current_alt > altimeter.altitude):
        current_alt = altimeter.altitude - ALT_DELTA_LANDED
        time.sleep(0.5)

    # Print landing data
    print("LZ Pressure: " + altimeter.pressure)
    lz_pressure = altimeter.pressure
    print("LZ Temp: " + altimeter.temperature)
    lz_temp = altimeter.temperature
    print("LZ Altitude: " + altimeter.altitude)
    lz_altitude = altimeter.altitude

    # Print postflight collected data
    print("Maximum Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2" % (accelerometer.acceleration))

    # Print battery state

    # Print survivability metrics

    # Transmit ground data back to the flight station

    # Save data to a file
