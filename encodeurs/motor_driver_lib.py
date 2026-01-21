import time



i2c = None

def init_i2c(i2c_instance):
    global i2c
    i2c = i2c_instance
    
REG = {'TYPE': 0x01,'DEADZONE': 0x02,'PWM': 0x07,'ENCODER_DELTA': [0x10, 0x11, 0x12, 0x13],}


def set_motor_parameters():
    i2c.writeto_mem(0x26, REG['TYPE'], bytearray([3]))
    time.sleep(0.05)
    i2c.writeto_mem(0x26, REG['DEADZONE'], bytearray([(value:=0)>>8 & 0xFF, value & 0xFF])) 
    time.sleep(0.05)

def control_motor_pwm(p1, p2, p3, p4):
    
    pwms = []
    for v in (p1, p2, p3, p4):
        pwms.extend([(v >> 8) & 0xFF, v & 0xFF])
    i2c.writeto_mem(0x26, REG['PWM'], bytearray(pwms)) 
    
    

    

    