from machine import Pin, ADC, PWM, I2C
from time import ticks_ms, sleep_ms
from i2c_lcd import I2cLcd
from neopixel import NeoPixel
import funcoesTCC
from inaLib import sensor_corrente
from ina219 import INA219

def map(value, in_min, in_max, out_min, out_max):
  scaled_value = int((value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)
  return scaled_value

lcd = I2cLcd(I2C(0), 0x27,4,20)
lcd.backlight_on()

# funcoesTCC.moduloRele(2,4)
rele = Pin(4, Pin.OUT)
rele.on()

setpoint = 140

neopixA = NeoPixel(Pin(32),30)
neopixB = NeoPixel(Pin(33),30)

listaDeCores = [(0,255,0),
                (0,255,0),
                (50,255,0),
                (50,255,0),
                (100,255,0),
                (100,255,0),
                (140,255,0),
                (140,255,0),
                (180,255,0),
                (180,255,0),
                (225,255,0),
                (225,255,0),
                (255,255,0),
                (255,255,0),
                (255,225,0),
                (255,225,0),
                (255,200,0),
                (255,200,0),
                (255,150,0),
                (255,150,0),
                (255,110,0),
                (255,110,0),
                (255,75,0),
                (255,75,0),
                (255,40,0),
                (255,40,0),
                (255,15,0),
                (255,15,0),
                (255,0,0),
                (255,0,0)]

for i, led in enumerate(listaDeCores):
    neopixA[i] = led
    neopixB[i] = led

neopixA.write()
neopixB.write()

tempoAnterior = 0
erroAnterior = 0

pot = ADC(Pin(34))
pot.atten(ADC.ATTN_11DB)

in1 = PWM(Pin(27), 5000)
in2 = PWM(Pin(26), 5000)

in3 = PWM(Pin(12), 5000)
in4 = PWM(Pin(14), 5000)

i2c = I2C(scl=18, sda=19)

motorInaA = INA219(i2c, 0X40)
motorInaA.set_calibration_32V_2A()

kp = 3
ki = 1/25
kd = 5
 
pwmMenorFoda = 620
pwmMenor = 620
oValorQTemQSerNegativo = 404

tempoAnterior = ticks_ms()
tempo = 0
deltaTempo = 0
somaErro = 0

while True:
    
    tempo = ticks_ms() - tempoAnterior

    angulo = map(pot.read_uv(), 1040949, 2138458, 0, 270)

    erro = setpoint - angulo
     
    somaErro = (erro*deltaTempo) + somaErro
    if somaErro > 75: somaErro = 75
    elif somaErro < -75: somaErro = -75
 
    deltaTempo = tempo - tempoAnterior
    deltaErro = erro  - erroAnterior
 
    p = kp * erro
    i = kp * ki * somaErro
    d = kp * kd * (deltaErro/deltaTempo)

    u = p + i + d
    
    motorA = map(u, 0, 270, pwmMenor, 1023)
    if motorA > 1023: motorA = 1023
    elif motorA < pwmMenorFoda: motorA = 0
    
    motorB = map(u, 270, 0, pwmMenor, 1023) - oValorQTemQSerNegativo
    if motorB > 1023: motorB = 1023
    elif motorB < pwmMenorFoda: motorB = 0
    
    in1.duty(motorA)
    in2.duty(motorB)
    in3.duty(motorA)
    in4.duty(motorB)
  
    print(f'A: {sensor_corrente(motorInaA)}')
        
    tempoAnterior = tempo
    erroAnterior = erro
    
    tempoAnterior = ticks_ms()
    
    sleep_ms(50)