#!/usr/bin/python

import os
import time
from GPSPoller import GPSPoller
from ParseAndStore import ParseAndStore
from can.interfaces.interface import Bus
import can
import MPU6050
from MPU6050 import MPU6050
from MPU6050 import MPU6050IRQHandler
import Adafruit_BBIO.GPIO as GPIO

GPS_logging = True
CAN_logging = True
MPU_logging = True

"""
Sleep a bit to allow the system to enable CAN interfaces
"""
time.sleep(5)

"""
All logging is based on threading.
The MPU logging is depending on IRQ on P9_11.
The GPS logging is depending on gpsd on ttyO5
The CAN logging is depending on enabling BB-DCAN1
"""
if GPS_logging:
    # Arguments are the log filename and if debugging is on or off
    os.system('gpsd /dev/ttyO5 -F /var/run/gpsd.sock')
    time.sleep(0.5)
    gps_thread = GPSPoller('./logs/gps.csv', False)
    gps_thread.start()

if CAN_logging:

    # can.rc['interface'] = 'socketcan_ctypes'
    can_interface = 'can0'
    bus = Bus(can_interface)
    # Arguments are the bus we're listening on and the function called on a
    # detected event.
    notifier = can.Notifier(bus, [ParseAndStore()])

if MPU_logging:
    i2c_bus = 1
    device_address = 0x68
    # The offsets are different for each device and should be changed to
    # sutiable figures using a calibration procedure
    x_accel_offset = -5489
    y_accel_offset = -1441
    z_accel_offset = 1305
    x_gyro_offset = -2
    y_gyro_offset = -72
    z_gyro_offset = -5
    enable_debug_output = False
    enable_logging = True
    log_file = './logs/mpulog.csv'

    mpu = MPU6050(i2c_bus, device_address, x_accel_offset,
                  y_accel_offset, z_accel_offset, x_gyro_offset,
                  y_gyro_offset, z_gyro_offset, enable_debug_output)
    mpuC = MPU6050IRQHandler(mpu, enable_logging, log_file)

    GPIO.setup("P9_11", GPIO.IN)
    GPIO.add_event_detect("P9_11", GPIO.RISING, callback=mpuC.action)

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    if GPS_logging:
        gps_thread.running = False
        gps_thread.join()
    if CAN_logging:
        bus.shutdown()
    if MPU_logging:
        GPIO.cleanup()
