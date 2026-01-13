from motor_driver_lib import REG
import main as mn






def read_encoder_deltas(): 
    ticks = []
    for reg in REG['ENCODER_DELTA']:
        buf = mn.i2c.readfrom_mem(0x26, reg, 2)
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
    # Hypothèse: N_ticks_tour_moteur = 52. 
    # omega_moteur = (ticks / dt) * (2 * pi / 52)
    # omega_roue = omega_moteur / Rapport_Reduction
    
    factor = (2 * 3.14159) / (52 * 0.01) # Sans réduction
    # Avec réduction (exemple R=30): factor /= 30
    
    for t in ticks:
        w = t * factor # Il faudra diviser par le rapport de réduction du moteur
        omegas.append(w)
    print(omegas)
    return omegas

calculate_omega_roue(read_encoder_deltas())



