from motor_driver_lib import REG
import main as mn






def read_encoder_deltas(): 
    ticks = []
    for reg in REG['ENCODER_DELTA']:
        buf = mn.i2c1.readfrom_mem(0x26, reg, 2)
        value = (buf[0] << 8) | buf[1]
        if value & 0x8000:
            value -= 0x10000
        ticks.append(value)
    return ticks 

def calculate_omega_roue(ticks):
    # ticks: liste des 4 valeurs de ticks mesurés sur 10ms (0.01s)
    omegas = []
    dt = 0.01 # 10 ms
        
    factor = (2 * 3.14159) / (60*52 * 0.01)
    
    for t in ticks:
        w = t * factor
        omegas.append(w)
    print("Omegas:", omegas)
    return omegas

calculate_omega_roue(read_encoder_deltas())



