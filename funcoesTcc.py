from machine import Pin, ADC, I2C
from time import sleep_ms
from i2c_lcd import I2cLcd


def tensaoBaixa():
  lcd = I2cLcd(I2C(0), 0x27,4,20)
  lcd.backlight_on()
  lcd.custom_char(0, bytearray([0x0E,0x00,0x0E,0x01,0x0F,0x11,0x0F,0x00]))
  lcd.custom_char(1, bytearray([0x00,0x00,0x00,0x04,0x0E,0x1F,0x0E,0x0E]))
  lcd.custom_char(2, bytearray([ 0x00,0x00,0x04,0x0E,0x1F,0x0E,0x0E,0x00]))
  lcd.custom_char(3, bytearray([0x00,0x04,0x0E,0x1F,0x0E,0x0E,0x00,0x00]))
  msg = 'Tensão muito baixa'
  msg1 ='Conecte uma fonte'
  msg2 = '12V'
  lcd.move_to(1,0)
  for i in msg:
    if i == 'ã':
        lcd.putchar(chr(0))
    else:
        lcd.putstr(i)
    sleep_ms(30)
  lcd.move_to(1,1)
  for i in msg1:
    lcd.putstr(i)
    sleep_ms(30)
  lcd.move_to(8,2)
  for i in msg2:
    lcd.putstr(i)
    sleep_ms(30)
  while True:
    lcd.move_to(0,3)
    lcd.putchar(chr(1))
    lcd.move_to(19,3)
    lcd.putchar(chr(1))
    sleep_ms(750)
    lcd.move_to(0,3)
    lcd.putchar(chr(2))
    lcd.move_to(19,3)
    lcd.putchar(chr(2))
    sleep_ms(100)
    lcd.move_to(0,3)
    lcd.putchar(chr(3))
    lcd.move_to(19,3)
    lcd.putchar(chr(3))
    sleep_ms(750)
    lcd.move_to(0,3)
    lcd.putchar(chr(2))
    lcd.move_to(19,3)
    lcd.putchar(chr(2))
    sleep_ms(100)
    
    
def tensaoAlta():
  lcd = I2cLcd(I2C(0), 0x27,4,20)
  lcd.backlight_on()
  lcd.custom_char(0, bytearray([0x0E,0x00,0x0E,0x01,0x0F,0x11,0x0F,0x00]))
  lcd.custom_char(1, bytearray([0x0E,0x11,0x1B,0x15,0x1B,0x0E,0x00,0x00]))
  lcd.custom_char(2, bytearray([0x00,0x0E,0x11,0x1B,0x15,0x0A,0x0E,0x00]))
  lcd.custom_char(3, bytearray([0x00,0x00,0x0E,0x11,0x1B,0x15,0x0A,0x0E]))
  msg = 'Tensão muito alta'
  msg1 ='Conecte uma fonte'
  msg2 = '12V'
  lcd.move_to(1,0)
  for i in msg:
    if i == 'ã':
        lcd.putchar(chr(0))
    else:
        lcd.putstr(i)
    sleep_ms(30)
  lcd.move_to(1,1)
  for i in msg1:
    lcd.putstr(i)
    sleep_ms(30)
  lcd.move_to(8,2)
  for i in msg2:
    lcd.putstr(i)
    sleep_ms(30)
  while True:
    lcd.move_to(0,3)
    lcd.putchar(chr(1))
    lcd.move_to(19,3)
    lcd.putchar(chr(1))
    sleep_ms(750)
    lcd.move_to(0,3)
    lcd.putchar(chr(2))
    lcd.move_to(19,3)
    lcd.putchar(chr(2))
    sleep_ms(100)
    lcd.move_to(0,3)
    lcd.putchar(chr(3))
    lcd.move_to(19,3)
    lcd.putchar(chr(3))
    sleep_ms(750)
    lcd.move_to(0,3)
    lcd.putchar(chr(2))
    lcd.move_to(19,3)
    lcd.putchar(chr(2))
    sleep_ms(100)

def ifrs():
  lcd = I2cLcd(I2C(0), 0x27,4,20)
  lcd.backlight_on()
  lcd.custom_char(0, bytearray([0x1F,0x1F,0x1F,0x1F,0x1F,0x1F,0x1F,0x1F])) #quadrado
  lcd.custom_char(1, bytearray([0x0E,0x1F,0x1F,0x1F,0x1F,0x1F,0x1F,0x0E])) #circulo
  lcd.custom_char(2, bytearray([0x0E,0x11,0x10,0x10,0x10,0x11,0x0E,0x04])) #Ç
  displayLinha0 = 'INSTITUTO FEDERAL'
  displayLinha1 = 'DO RIO GRANDE, RS' 
  ano = '2023'
  vazio = ' '
  lcd.move_to(0,0)
  lcd.putchar(chr(1))
  sleep_ms(50)
  lcd.putchar(chr(0))
  sleep_ms(50)
  lcd.putchar(chr(0))
  sleep_ms(50)
  lcd.move_to(0,1)
  lcd.putchar(chr(0))
  sleep_ms(50)
  lcd.putchar(chr(0))
  sleep_ms(50)
  lcd.move_to(0,2)
  lcd.putchar(chr(0))
  sleep_ms(50)
  lcd.putchar(chr(0))
  sleep_ms(50)
  lcd.putchar(chr(0))
  sleep_ms(50)
  lcd.move_to(0,3)
  lcd.putchar(chr(0))
  sleep_ms(50)
  lcd.putchar(chr(0))
  sleep_ms(500)
  lcd.move_to(3,0)
  for i in displayLinha0:
    lcd.putstr(i)
    sleep_ms(50)
  lcd.move_to(3,1)
  for i in displayLinha1:
    lcd.putstr(i)
    sleep_ms(50)
  lcd.move_to(16,3)
  for i in ano:
    lcd.putstr(i)
    sleep_ms(50)
  sleep_ms(3000)
  lcd.move_to(0,0)
  for i in range(43):
    lcd.putstr(vazio)
    sleep_ms(5)
  lcd.move_to(0,3)
  for i in range(2):
    lcd.putstr(vazio)
    sleep_ms(50)
  lcd.move_to(16,3)
  for i in range(4):
    lcd.putstr(vazio)
    sleep_ms(50)
  sleep_ms(1000)
  logo()
  
def logo():
  lcd = I2cLcd(I2C(0), 0x27,4,20)
  lcd.custom_char(0, bytearray([0x04,0x04,0x04,0x04,0x0E,0x0E,0x1F,0x1F]))#base
  lcd.custom_char(1, bytearray([0x04,0x04,0x04,0x04,0x04,0x04,0x04,0x04]))#vertical
  lcd.custom_char(2, bytearray([0x00,0x00,0x1F,0x00,0x00,0x00,0x00,0x00]))#horizontal
  lcd.custom_char(3, bytearray([0x0E,0x1F,0x1B,0x1F,0x1F,0x0E,0x04,0x04]))#topo
  lcd.custom_char(4, bytearray([0x1F,0x04,0x1E,0x0E,0x00,0x00,0x00,0x00]))#motorR
  lcd.custom_char(5, bytearray([0x1F,0x04,0x0F,0x0E,0x00,0x00,0x00,0x00]))#motorL
  lcd.custom_char(6, bytearray([0x00,0x00,0x00,0x00,0x00,0x1F,0x1F,0x1F]))#retang
  lcd.custom_char(7, bytearray([0x1F,0x1F,0x1F,0x1F,0x1F,0x1F,0x1F,0x1F]))#quadrado
  vazio = ' '
  # S
  lcd.move_to(2,0)
  lcd.putchar(chr(7))
  sleep_ms(50)
  lcd.move_to(1,0)
  lcd.putchar(chr(7))
  sleep_ms(50)
  lcd.move_to(0,0)
  lcd.putchar(chr(7))
  sleep_ms(50)
  lcd.move_to(0,1)
  lcd.putchar(chr(7))
  sleep_ms(50)
  lcd.move_to(1,1)
  for i in range(2):
    lcd.putchar(chr(6))
    sleep_ms(50)
  lcd.move_to(2,2)
  lcd.putchar(chr(7))
  sleep_ms(50)
  lcd.move_to(2,3)
  lcd.putchar(chr(7))
  sleep_ms(50)
  lcd.move_to(1,3)
  lcd.putchar(chr(7))
  sleep_ms(50)
  lcd.move_to(0,3)
  lcd.putchar(chr(7))
  sleep_ms(50)
  # P
  lcd.move_to(4,3)
  lcd.putchar(chr(7))
  sleep_ms(50)
  lcd.move_to(4,2)
  lcd.putchar(chr(7))
  sleep_ms(50)
  lcd.move_to(4,1)
  lcd.putchar(chr(7))
  sleep_ms(50)
  lcd.move_to(4,0)
  for i  in range(3):
    lcd.putchar(chr(7))
    sleep_ms(50)
  lcd.move_to(6,1)
  lcd.putchar(chr(7))
  sleep_ms(50)
  lcd.move_to(6,2)
  lcd.putchar(chr(7))
  sleep_ms(50)
  lcd.move_to(5,2)
  lcd.putchar(chr(7))
  sleep_ms(50)
  lcd.move_to(4,2)
  lcd.putchar(chr(7))
  sleep_ms(50)
  # A
  lcd.move_to(8,3)
  lcd.putchar(chr(7))
  sleep_ms(50)
  lcd.move_to(8,2)
  lcd.putchar(chr(7))
  sleep_ms(50)
  lcd.move_to(8,1)
  lcd.putchar(chr(7))
  sleep_ms(50)
  lcd.move_to(8,0)
  for i in range(3):
    lcd.putchar(chr(7))
    sleep_ms(50)
  lcd.move_to(10,1)
  lcd.putchar(chr(7))
  sleep_ms(50)
  lcd.move_to(10,2)
  lcd.putchar(chr(7))
  sleep_ms(50)
  lcd.move_to(10,3)
  lcd.putchar(chr(7))
  sleep_ms(50)
  lcd.move_to(9,2)
  lcd.putchar(chr(7))
  sleep_ms(50)
  # simbolo
  lcd.move_to(16,3)
  lcd.putchar(chr(0))
  sleep_ms(50)
  lcd.move_to(16,2)
  lcd.putchar(chr(1))
  sleep_ms(50)
  lcd.move_to(16,1)
  lcd.putchar(chr(1))
  sleep_ms(50)
  lcd.move_to(13,0)
  lcd.putchar(chr(5))
  sleep_ms(50)
  lcd.putchar(chr(2))
  sleep_ms(50)
  lcd.putchar(chr(2))
  sleep_ms(50)
  lcd.putchar(chr(3))
  sleep_ms(50)
  lcd.putchar(chr(2))
  sleep_ms(50)
  lcd.putchar(chr(2))
  sleep_ms(50)
  lcd.putchar(chr(4))
  sleep_ms(3000)
  # simbolo apaga
  lcd.move_to(16,3)
  lcd.putstr(vazio)
  sleep_ms(50)
  lcd.move_to(16,2)
  lcd.putstr(vazio)
  sleep_ms(50)
  lcd.move_to(16,1)
  lcd.putstr(vazio)
  sleep_ms(50)
  lcd.move_to(13,0)
  lcd.putstr(vazio)
  sleep_ms(50)
  lcd.putstr(vazio)
  sleep_ms(50)
  lcd.putstr(vazio)
  sleep_ms(50)
  lcd.putstr(vazio)
  sleep_ms(50)
  lcd.putstr(vazio)
  sleep_ms(50)
  lcd.putstr(vazio)
  sleep_ms(50)
  lcd.putstr(vazio)
  # A apaga
  lcd.move_to(8,3)
  lcd.putstr(vazio)
  sleep_ms(30)
  lcd.move_to(8,2)
  lcd.putstr(vazio)
  sleep_ms(30)
  lcd.move_to(8,1)
  lcd.putstr(vazio)
  sleep_ms(30)
  lcd.move_to(8,0)
  for i in range(3):
    lcd.putstr(vazio)
    sleep_ms(30)
  lcd.move_to(10,1)
  lcd.putstr(vazio)
  sleep_ms(30)
  lcd.move_to(10,2)
  lcd.putstr(vazio)
  sleep_ms(30)
  lcd.move_to(10,3)
  lcd.putstr(vazio)
  sleep_ms(30)
  lcd.move_to(9,2)
  lcd.putstr(vazio)
  sleep_ms(30)
  # P apaga
  lcd.move_to(4,3)
  lcd.putstr(vazio)
  sleep_ms(30)
  lcd.move_to(4,2)
  lcd.putstr(vazio)
  sleep_ms(30)
  lcd.move_to(4,1)
  lcd.putstr(vazio)
  sleep_ms(30)
  lcd.move_to(4,0)
  for i  in range(3):
    lcd.putstr(vazio)
    sleep_ms(30)
  lcd.move_to(6,1)
  lcd.putstr(vazio)
  sleep_ms(30)
  lcd.move_to(6,2)
  lcd.putstr(vazio)
  sleep_ms(30)
  lcd.move_to(5,2)
  lcd.putstr(vazio)
  sleep_ms(30)
  lcd.move_to(4,2)
  lcd.putstr(vazio)
  sleep_ms(30)
  # S apaga
  lcd.move_to(2,0)
  lcd.putstr(vazio)
  sleep_ms(30)
  lcd.move_to(1,0)
  lcd.putstr(vazio)
  sleep_ms(30)
  lcd.move_to(0,0)
  lcd.putstr(vazio)
  sleep_ms(30)
  lcd.move_to(0,1)
  lcd.putstr(vazio)
  sleep_ms(30)
  lcd.move_to(1,1)
  for i in range(2):
    lcd.putstr(vazio)
    sleep_ms(30)
  lcd.move_to(2,2)
  lcd.putstr(vazio)
  sleep_ms(30)
  lcd.move_to(2,3)
  lcd.putstr(vazio)
  sleep_ms(30)
  lcd.move_to(1,3)
  lcd.putstr(vazio)
  sleep_ms(30)
  lcd.move_to(0,3)
  lcd.putstr(vazio)
  sleep_ms(1000)
  opcoes()

def moduloRele(PinIn, PinOut):
    divisor = ADC(Pin(PinIn))
    divisor.atten(ADC.ATTN_11DB)
    rele = Pin(PinOut, Pin.OUT)
    tensao = 0
    for i in range(20):
        tensao += adc.read()
    media = tensao/20
    if media < 1550:
        tensaoBaixa()
    elif media > 1700:
        tensaoAlta()
    elif media >= 1550 and media <= 1700:
        rele.on()
        ifrs()
        
    

        
        
        
        
        