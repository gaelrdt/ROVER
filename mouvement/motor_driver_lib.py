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
    
    

    
def read_encoder_deltas(): 
    ticks = []
    for reg in REG['ENCODER_DELTA']:
        buf = i2c.readfrom_mem(0x26, reg, 2)
        value = (buf[0] << 8) | buf[1]
        if value & 0x8000:
            value -= 0x10000
            ticks.append(value)
    return ticks 

def calculate_omega_roue(ticks):
    # ticks: liste des 4 valeurs de ticks mesurés sur 10ms (0.01s)
    omegas = []
    dt = 0.01 # 10 ms
    # Remplacer TICKS_PER_RAD par la valeur physique calculée (52 * Reduction / 2pi)
    # Si le rapport de réduction n'est pas connu, utiliser une constante à calibrer.
    # Hypothèse: N_ticks_tour_moteur = 52. 
    # omega_moteur = (ticks / dt) * (2 * pi / 52)
    # omega_roue = omega_moteur / Rapport_Reduction
    
    factor = (2 * 3.14159) / (52 * 0.01) # Sans réduction
    # Avec réduction (exemple R=30): factor /= 30
    
    for t in ticks:
        w = t * factor # Il faudra diviser par le rapport de réduction du moteur
        omegas.append(w)
    print("Omegas:", omegas)
    return omegas

calculate_omega_roue(read_encoder_deltas())
    