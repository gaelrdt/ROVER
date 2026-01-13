from machine import I2C, Pin # type: ignore
import time
import motor_driver_lib as mdl

i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=400000)

mdl.init_i2c(i2c)
mdl.set_motor_parameters()
mdl.control_motor_pwm(2100, 2100, 2100, 2100)




