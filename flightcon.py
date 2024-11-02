# Imports
import time
import busio
from board import *
from adafruit_bus_device.i2c_device import I2CDevice
import adafruit_mpl3115a2
from adafruit_lsm6ds.ism330dhcx import ISM330DHCX
from datetime import datetime

required_alt = 1000

def preflight_check(altimeter, ground_alt):
    if(max((altimeter.altitude - ground_alt), 0) > required_alt):
        print("Triggered with delta " + str(altimeter.altitude - ground_alt))
        return True
    return False

# Start main
armed = False
# Pressure is in pascals, 1 kPa = 1000 Pa
sea_pressure = 102268
# Var defines
max_alt = 0
max_x_accel, max_y_accel, max_z_accel = 0

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

    #init record file
    outfile = open("log-" + datetime.now().strftime("%d-%m-%Y_%H:%M:%S") + ".txt", "w")

    #Get original pressure/temp/alt
    init_pressure = altimeter.pressure
    print("Init pressure: " + str(init_pressure))
    init_temp = altimeter.temperature
    print("Init temperature: " + str(init_temp))
    init_alt = altimeter.altitude
    print("Init altitude: " + str(init_alt))


    # Check every second to see if we've started flying
    while not preflight_check(altimeter, init_alt):
        # Do accel stuff
        x, y, z = accelerometer.acceleration
        if(x > max_x_accel):
            max_x_accel = x
        if(y > max_y_accel):
            max_y_accel = y
        if(z > max_z_accel):
            max_z_accel = z

        # Sleep until we launch
        time.sleep(0.5)

    armed = True
    print("Arming triggered")
    outfile.write("Armed at time: " + datetime.now().strftime("%H:%M:%S"))
   
    # Continuously poll max_alt until we hit apogee and start coming down again
    # Starts at our initial ground altitude
    max_alt = init_alt
    while altimeter.altitude > max_alt:
        max_alt = altimeter.altitude
        # Do accel stuff
        x, y, z = accelerometer.acceleration
        if(x > max_x_accel):
            max_x_accel = x
        if(y > max_y_accel):
            max_y_accel = y
        if(z > max_z_accel):
            max_z_accel = z

        time.sleep(0.5)

    # Do apogee-based stuff
    print("Apogee: " + str(max_alt))

    # Wait for the rocket to land, then collect ground data
    current_alt = altimeter.altitude - ALT_DELTA_LANDED
    while(not (current_alt < (init_alt + required_alt)) or current_alt > altimeter.altitude):
        current_alt = altimeter.altitude - ALT_DELTA_LANDED
        # Do accel stuff
        x, y, z = accelerometer.acceleration
        if(x > max_x_accel):
            max_x_accel = x
        if(y > max_y_accel):
            max_y_accel = y
        if(z > max_z_accel):
            max_z_accel = z
        time.sleep(0.5)

    # Print landing data
    print("LZ Pressure: " + str(altimeter.pressure))
    lz_pressure = altimeter.pressure
    outfile.write(str(lz_pressure))
    print("LZ Temp: " + str(altimeter.temperature))
    lz_temp = altimeter.temperature
    outfile.write(str(lz_temp))
    print("LZ Altitude: " + str(altimeter.altitude))
    lz_altitude = altimeter.altitude
    outfile.write(str(lz_altitude))

    # Print postflight collected data
    print("Final gyro: X:%.2f, Y: %.2f, Z: %.2f m/s^2" % (accelerometer.gyro))
    outfile.write("Final gyro: X:%.2f, Y: %.2f, Z: %.2f m/s^2" % (accelerometer.gyro))

    # Print battery state

    # Print survivability metrics

    # Transmit ground data back to the flight station

    # Close our file up
    outfile.close()