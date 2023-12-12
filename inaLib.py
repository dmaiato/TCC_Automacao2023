from machine import Pin, I2C
from time import sleep_ms, ticks_ms
from ina219 import INA219

def sensor_corrente(ina):
    corrente = ina.current * 0.815
    tensao = (corrente / 1000) * 9.4 
    potencia = corrente * tensao
    return corrente, tensao, potencia
    
    
    
    