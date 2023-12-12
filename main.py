from machine import Pin, I2C, ADC, PWM
from umqtt.robust import MQTTClient
from i2c_lcd import I2cLcd
from rotary import Rotary
from utime import ticks_ms, sleep_ms
from gc import collect
from neopixel import NeoPixel
from screens import Lcd_Screens
from funcs import wifi_connect, clamp, map
from ujson import load, dumps

#############################################################################
# setups e funções

with open("cfg.json", "r") as arq:
	cfg = load(arq)

selection = Rotary(15, 22, 21)
cx, cy = 0, 0 # cursor

stockDict = {"ganhos": [[0,0,0,0], [0,0,0,0], [0,0,0,0]],
             "setpoint": [1,3,5], "voltar": False,
						 "retry": True, "modo": "offline"}

bufferDict = dict(stockDict)

stockValues = {"ganhos": {"kp": 0.0, 'ki': 0.0, 'kd': 0.0},
		  	   "setpoint": 135}

values = dict(stockValues)

state = "none"

lcd = I2cLcd(I2C(0), 0x27, 4, 20) 
rele = Pin(4, Pin.OUT)
rele.on()
neopixA = NeoPixel(Pin(32),30)
neopixB = NeoPixel(Pin(33),30)

posAnterior = 10

def callback(t, p):
	topico = t.decode()
	cmd = load(p.decode())

	values["ganhos"].update(cmd, cmd)

	print(values["ganhos"])

def rotary_changed(change): # máquina de estados

	print(change)

	global tela, state, block, lcd, values, cx, cy, posAnterior

	print(bufferDict["voltar"])

	if tela.name == "setpoint":
		cursor_tuples = (10, 11, 12)
		cy = 2

		buff = bufferDict['setpoint']

		if change == Rotary.ROT_CW:
			buff[cx] = (buff[cx] + 1) % 10
		
		elif change == Rotary.ROT_CCW:
			buff[cx] -= 1

		elif change == Rotary.SW_PRESS:
			state = "init"
			return

		elif change == Rotary.SW_RELEASE:
			state = "none"
			if tela.block: return
			cx = (cx +1) % len(cursor_tuples)
			lcd.move_to(cursor_tuples[cx], 0)
			posAnterior = cursor_tuples[cx]
			return

		if cx == 0:
			buff[cx] = clamp(buff[cx], 2)

			if buff[0] == 2 and buff[1] > 7:
				lcd.hide_cursor()
				lcd.move_to(11,0)
				lcd.overwrite("7")
				if buff[2] > 0:
					lcd.move_to(12, 0)
					lcd.overwrite("0")
				buff[1] = 7
				buff[2] = 0
				lcd.move_to(10,0)
				lcd.show_cursor()

		elif cx == 1:
			if buff[0] == 2:
				buff[cx] = clamp(buff[cx], 7)

				if buff[cx] == 7 and buff[2] > 0:
					lcd.hide_cursor()
					lcd.move_to(12,0)
					lcd.overwrite("0")
					lcd.move_to(11,0)
					lcd.show_cursor()
					buff[2] = 0
			else:
				buff[cx] = clamp(buff[cx], 9)

		elif cx == 2:
			if buff[0] == 2 and buff[1] == 7:
				buff[2] = 0
			else:
				buff[cx] = clamp(buff[cx], 9)

		bufferDict['setpoint'] = buff

		values[tela.name] = int(''.join((str(i) for i in bufferDict[tela.name])))
		print(values[tela.name])

		if tela.block == False:
			lcd.overwrite(str(buff[cx]))

	elif tela.name == "modo_on_offline":
		cursor_tuple = (1, 11)

		cy = 2

		if change == Rotary.SW_PRESS:
			state = "init"

		elif change == Rotary.SW_RELEASE:
			state = "none"
			cx += 1

		cx = clamp(cx, 1)

		if cx: bufferDict["modo"] = "online"
		else: bufferDict["modo"] = "offline"

		if tela.block == False:
			lcd.hide_cursor()
			lcd.overwrite(' ')
			lcd.move_to(cursor_tuple[cx], cy)
			lcd.overwrite("~")
	
	elif tela.name == "online":

		if change == Rotary.SW_PRESS:
			state = "init"

		elif change == Rotary.SW_RELEASE:
			state = "none"
  
	elif tela.name == "offline":
		# 9, 10, 12, 13

		cursor_tuple = (4,5,7,8,12)
		buff = bufferDict['ganhos']

		if change == Rotary.ROT_CW:
			if cx == 4 and cy == 2: return
			buff[cy][cx] = clamp(buff[cy][cx] + 1, 9)
		
		elif change == Rotary.ROT_CCW:
			if cx == 4 and cy == 2: return
			buff[cy][cx] = clamp(buff[cy][cx] - 1, 9)

		elif change == Rotary.SW_PRESS:
			state = "init"

			if cx == 4:
				bufferDict['voltar'] = True

			return

		elif change == Rotary.SW_RELEASE:
			state = "none"
			if tela.block: return
			cx += 1

			if cy == 2:
				if cx > 4: cy +=1
				cx %= 5
				cy %= 3
			
			else:
				if cx > 3: cy +=1
				cx %= 4
				cy %= 3

			bufferDict['voltar'] = False

		if not tela.block:
			lcd.hide_cursor()
			lcd.move_to(cursor_tuple[cx], cy+1)
			if cx == 0 and cy == 0:
				lcd.move_to(12, 3)
				lcd.overwrite(' ')
				lcd.move_to(4, 1)
				lcd.overwrite(str(buff[cy][cx]))
			elif cy != 2 or cx != 4:
				lcd.overwrite(str(buff[cy][cx]))
			else: lcd.overwrite('~')
			lcd.show_cursor()

	elif tela.name == "erro_conexao":
		cursor_tuple = (1, 14)

		cy = 2

		if change == Rotary.SW_PRESS:
			state = "init"
			return

		elif change == Rotary.SW_RELEASE:
			state = "none"
			cx += 1

		cx = clamp(cx, 1)

		if cx: bufferDict["retry"] = False
		else: bufferDict["retry"] = True

		print(bufferDict["retry"])

		if tela.block == False:
			lcd.hide_cursor()
			lcd.overwrite(' ')
			lcd.move_to(cursor_tuple[cx], cy)
			lcd.overwrite("~")

	collect()
	print(state)

selection.add_handler(rotary_changed) # passa o callback para o objeto do encoder

tela = Lcd_Screens(lcd) # envia o objeo do lcd para a classe mestre de telas
tela.modo_on_offline()

#############################################################################
# Elementos de controle

tempoAnterior = 0
erroAnterior = 0

pot = ADC(Pin(34))
pot.atten(ADC.ATTN_11DB)

in1 = PWM(Pin(27), 5000)
in2 = PWM(Pin(26), 5000)

in3 = PWM(Pin(12), 5000)
in4 = PWM(Pin(14), 5000)

kp = 3
ki = 1/20
kd = 35

pwmMenorFoda = 620
pwmMenor = 620
oValorQTemQSerNegativo = 404

tempoAnterior = ticks_ms()
tempo = 0
deltaTempo = 0
somaErro = 0

#############################################################################
# loop principal e máquina de estados

print("________________________________________________")

rotina = "offline"
topAttr = b"v1/devices/me/attributes"
delay = 0

# Checagem de tensão

shutdown = False
divisor = ADC(Pin(2))
divisor.atten(ADC.ATTN_11DB)
rele = Pin(4, Pin.OUT)
tensao = 0
for i in range(20):
	tensao += divisor.read()
media = tensao/20
media = 1600
if media < 1550:
	shutdown = True
	tela.tensao_baixa()
elif media > 1700:
	shutdown = True
	tela.tensao_alta()
else:
	rele.on()

t_angulo = 0
t_erro = 0
delayDisplay = 0

while not shutdown:

	if state == "init":
			delay = ticks_ms() + 3000
			state = "countdown"

	if rotina == "offline":
		
		if ticks_ms() < delay:
			continue

		if state != "countdown": 
			continue

		state = "none"
		delay = 0
		cx, cy = 0, 0

		if tela.name == "modo_on_offline":
			if bufferDict["modo"] == "online":
				rotina = "iniciando_conexao"
				tela.iniciando_conexao()
			else:
				tela.offline()

		elif tela.name == "online":
			bufferDict["modo"] = "offline"
			tela.modo_on_offline()

		elif tela.name == "offline":
			valores = values['ganhos']
			if bufferDict['voltar']:
				for i, e in enumerate(bufferDict["ganhos"]):
					bufferDict["ganhos"][i] = [0,0,0,0]
				for i in list(values["ganhos"].keys()):
					values["ganhos"][i] = 0.0
				tela.modo_on_offline()
				bufferDict["modo"] = "offline"
				cx, cy = 0, 0
				continue
			valores['kp'] = float(''.join(str(i) for i in bufferDict['ganhos'][0])) / 100
			valores['ki'] = float(''.join(str(i) for i in bufferDict['ganhos'][1])) / 100
			valores['kd'] = float(''.join(str(i) for i in bufferDict['ganhos'][2])) / 100
			print(valores['kp'], valores['ki'], valores['kd'])

			rotina = "inicializacao_pid"
			tela.setpoint()

	elif rotina == "iniciando_conexao":

		try:
			wifi = wifi_connect(cfg["rede"], cfg["senha"])
			mqtt = MQTTClient(cfg['id'], cfg['broker'], user = cfg['token'], password = cfg['mqtt_pw'])
			mqtt.set_callback(callback)
			mqtt.connect()
			print ('requests')
			mqtt.subscribe(topAttr)
			mqtt.publish(topAttr, dumps(values["ganhos"]).encode())
		except:
			rotina = "erro_conexao"
			tela.erro_conexao()
			sleep_ms(2000)
			continue

		rotina = "online"
		tela.online()

	elif rotina == "erro_conexao":
		if ticks_ms() < delay:
			continue
		if state != "countdown": 
			continue
		state = "none"
		delay = 0

		if bufferDict["retry"]:
			rotina = "iniciando_conexao"
			tela.iniciando_conexao()
		else:
			rotina = "offline"
			bufferDict["modo"] = "offline"
			tela.modo_on_offline()

		cx, cy = 0, 0

	elif rotina == "online":

		mqtt.check_msg()
		if not wifi.isconnected():
			rotina = "iniciando_conexao"
			tela.iniciando_conexao()
			continue

		if ticks_ms() < delay:
			continue
		if state != "countdown": 
			continue
		state = "none"
		delay = 0

		wifi.disconnect()

		cx, cy = 0, 0
		rotina = "offline"
		bufferDict["modo"] = "offline"
		tela.modo_on_offline()

	elif rotina == "inicializacao_pid":

		setpoint = int(values["setpoint"])
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

		tempoAnterior = 0
		erroAnterior = 0

		pot = ADC(Pin(34))
		pot.atten(ADC.ATTN_11DB)

		in1 = PWM(Pin(27), 5000)
		in2 = PWM(Pin(26), 5000)

		in3 = PWM(Pin(12), 5000)
		in4 = PWM(Pin(14), 5000)

		kp = 3
		ki = 1/20
		kd = 35

		pwmMenorFoda = 620
		pwmMenor = 620
		compensador = 404

		tempoAnterior = ticks_ms()
		tempo = 0
		deltaTempo = 0
		somaErro = 0

		delayDisplay = ticks_ms() + 750

		rotina = "pid"

	elif rotina == "pid":

		if bufferDict["modo"] == "online":
			mqtt.check_msg()
			if not wifi.isconnected():
				rotina = "iniciando_conexao"
				tela.iniciando_conexao()
				continue

		setpoint = values["setpoint"]
		tempo = ticks_ms() - tempoAnterior
		angulo = map(pot.read_uv(), 1040949, 2138458, 0, 270)
		erro = setpoint - angulo
		
		somaErro = (erro*deltaTempo) + somaErro
		if somaErro > 75: somaErro = 75
		elif somaErro < -75: somaErro = -75

		deltaTempo = tempo - tempoAnterior
		deltaErro = erro  - erroAnterior

		ganhos = values["ganhos"]

		p = ganhos["kp"] * erro
		i = ganhos["kp"] * ganhos["ki"] * somaErro
		d = ganhos["kp"] * ganhos["kp"] * (deltaErro/deltaTempo)

		u = p + i + d
		
		motorA = map(u, 0, 270, pwmMenor, 1023)
		if motorA > 1023: motorA = 1023
		elif motorA < pwmMenorFoda: motorA = 0
		
		motorB = map(u, 270, 0, pwmMenor, 1023) - compensador
		if motorB > 1023: motorB = 1023
		elif motorB < pwmMenorFoda: motorB = 0
		
		in1.duty(motorA)
		in2.duty(motorB)
		in3.duty(motorA)
		in4.duty(motorB)
	
		print(f'{angulo} {setpoint}')
				
		tempoAnterior = tempo
		erroAnterior = erro
		
		tempoAnterior = ticks_ms()

		if ticks_ms() >= delayDisplay:
			tela.block = True
			lcd.hide_cursor()
			t_angulo = (t_angulo + 10) % 110
			t_erro = (t_erro + 10) % 110

			lcd.move_to(8, 2)
			lcd.putstr("   ")
			lcd.move_to(8, 2)
			lcd.putstr(f"{t_angulo}")
			print(t_angulo)
			lcd.move_to(8, 3)
			lcd.putstr("   ")
			lcd.move_to(8, 3)
			lcd.putstr(f"{t_erro}")

			lcd.move_to(posAnterior, 0)
			delayDisplay = ticks_ms() + 750
			tela.block = False
			lcd.show_cursor()

		if ticks_ms() < delay:
			continue
		if state != "countdown": 
			continue

		state = "none"
		delay = 0

		if tela.name == "online":
			in1.duty(0)
			in2.duty(0)
			in3.duty(0)
			in4.duty(0)
			wifi.disconnect()
			bufferDict["setpoint"] = [1,3,5]
			values["setpoint"] = 135
			for i, e in enumerate(bufferDict["ganhos"]):
				bufferDict["ganhos"][i] = [0,0,0,0]
			for i in list(values["ganhos"].keys()):
				values["ganhos"][i] = 0.0
			print(values['ganhos'])
			rotina = "modo_on_offline"
			cx, cy = 0, 0
			tela.modo_on_offline()

		if tela.name == "setpoint":
			in1.duty(0)
			in2.duty(0)
			in3.duty(0)
			in4.duty(0)
			bufferDict["setpoint"] = [1,3,5]
			values["setpoint"] = 135
			for i, e in enumerate(bufferDict["ganhos"]):
				bufferDict["ganhos"][i] = [0,0,0,0]
			for i in list(values["ganhos"].keys()):
				values["ganhos"][i] = 0.0
			print(values['ganhos'])
			rotina = "offline"
			cx, cy = 0, 0
			tela.offline()

	collect()
		
