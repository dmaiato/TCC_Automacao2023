from time import sleep_ms
from gc import collect

class Lcd_Screens:
	def __init__(self, display: object):
		self.lcd = display
		self.lcd.backlight_on()
		self.block = False
		self.cursor = 0
		self.name = ''

	def mestre(func: object):
		def pacote(self, *args, **kwargs):
			self.lcd.hide_cursor()
			self.lcd.clear()
			self.block = True
			retornoFunc = func(self, *args, **kwargs)
			self.block = False
			collect()
			return retornoFunc
		return pacote

	@mestre
	def inicializacao(self):
		self.lcd.custom_char(0, bytearray([0x1F,0x1F,0x1F,0x1F,0x1F,0x1F,0x1F,0x1F])) #quadrado
		self.lcd.custom_char(1, bytearray([0x0E,0x1F,0x1F,0x1F,0x1F,0x1F,0x1F,0x0E])) #circulo
		self.lcd.custom_char(2, bytearray([0x0E,0x11,0x10,0x10,0x10,0x11,0x0E,0x04])) #Ç
		self.lcd.move_to(0,0)
		self.lcd.putchar(chr(1))
		for i in range(2): self.lcd.putchar(chr(0)) 
		self.lcd.move_to(0,1)
		for i in range(2): self.lcd.putchar(chr(0)) 
		self.lcd.move_to(0,2)
		for i in range(3): self.lcd.putchar(chr(0)) 
		self.lcd.move_to(0,3)
		for i in range(2): self.lcd.putchar(chr(0)) 
		self.lcd.move_to(3,0)
		self.lcd.putstr('INSTITUTO FEDERAL')
		self.lcd.move_to(3,1)
		self.lcd.putstr('DO RIO GRANDE, RS')
		self.lcd.move_to(16,3)
		self.lcd.putstr('2023')
		
		sleep_ms(3000)
		self.logo()

	@mestre
	def logo(self):
		self.lcd.custom_char(0, bytearray([0x04,0x04,0x04,0x04,0x0E,0x0E,0x1F,0x1F]))#base
		self.lcd.custom_char(1, bytearray([0x04,0x04,0x04,0x04,0x04,0x04,0x04,0x04]))#vertical
		self.lcd.custom_char(2, bytearray([0x00,0x00,0x1F,0x00,0x00,0x00,0x00,0x00]))#horizontal
		self.lcd.custom_char(3, bytearray([0x0E,0x1F,0x1B,0x1F,0x1F,0x0E,0x04,0x04]))#topo
		self.lcd.custom_char(4, bytearray([0x1F,0x04,0x1E,0x0E,0x00,0x00,0x00,0x00]))#motorR
		self.lcd.custom_char(5, bytearray([0x1F,0x04,0x0F,0x0E,0x00,0x00,0x00,0x00]))#motorL
		self.lcd.custom_char(6, bytearray([0x00,0x00,0x00,0x00,0x00,0x1F,0x1F,0x1F]))#retang
		self.lcd.custom_char(7, bytearray([0x1F,0x1F,0x1F,0x1F,0x1F,0x1F,0x1F,0x1F]))#quadrado
		# S
		self.lcd.move_to(2,0)
		self.lcd.putchar(chr(7))
		self.lcd.move_to(1,0)
		self.lcd.putchar(chr(7))
		self.lcd.move_to(0,0)
		self.lcd.putchar(chr(7))
		self.lcd.move_to(0,1)
		self.lcd.putchar(chr(7))
		self.lcd.move_to(1,1)
		for i in range(2):
			self.lcd.putchar(chr(6))
		self.lcd.move_to(2,2)
		self.lcd.putchar(chr(7))
		self.lcd.move_to(2,3)
		self.lcd.putchar(chr(7))
		self.lcd.move_to(1,3)
		self.lcd.putchar(chr(7))
		self.lcd.move_to(0,3)
		self.lcd.putchar(chr(7))
		# P
		self.lcd.move_to(4,3)
		self.lcd.putchar(chr(7))
		self.lcd.move_to(4,2)
		self.lcd.putchar(chr(7))
		self.lcd.move_to(4,1)
		self.lcd.putchar(chr(7))
		self.lcd.move_to(4,0)
		for i  in range(3):
			self.lcd.putchar(chr(7))
		self.lcd.move_to(6,1)
		self.lcd.putchar(chr(7))
		self.lcd.move_to(6,2)
		self.lcd.putchar(chr(7))
		self.lcd.move_to(5,2)
		self.lcd.putchar(chr(7))
		self.lcd.move_to(4,2)
		self.lcd.putchar(chr(7))
		# A
		self.lcd.move_to(8,3)
		self.lcd.putchar(chr(7))
		self.lcd.move_to(8,2)
		self.lcd.putchar(chr(7))
		self.lcd.move_to(8,1)
		self.lcd.putchar(chr(7))
		self.lcd.move_to(8,0)
		for i in range(3):
			self.lcd.putchar(chr(7))
		self.lcd.move_to(10,1)
		self.lcd.putchar(chr(7))
		self.lcd.move_to(10,2)
		self.lcd.putchar(chr(7))
		self.lcd.move_to(10,3)
		self.lcd.putchar(chr(7))
		self.lcd.move_to(9,2)
		self.lcd.putchar(chr(7))
		# simbolo
		self.lcd.move_to(16,3)
		self.lcd.putchar(chr(0))
		self.lcd.move_to(16,2)
		self.lcd.putchar(chr(1))
		self.lcd.move_to(16,1)
		self.lcd.putchar(chr(1))
		self.lcd.move_to(13,0)
		self.lcd.putchar(chr(5))
		self.lcd.putchar(chr(2))
		self.lcd.putchar(chr(2))
		self.lcd.putchar(chr(3))
		self.lcd.putchar(chr(2))
		self.lcd.putchar(chr(2))
		self.lcd.putchar(chr(4))

		sleep_ms(3000)
		self.modo_on_offline()

	@mestre
	def modo_on_offline(self):
		self.name = 'modo_on_offline'
		self.lcd.move_to(3, 0)
		self.lcd.putstr("Escolha o modo")
		self.lcd.move_to(2, 2)
		self.lcd.putstr("offline")
		self.lcd.move_to(12, 2)
		self.lcd.putstr("online")
		self.lcd.move_to(1, 2)
		self.lcd.overwrite("~")

	@mestre
	def iniciando_conexao(self):
		self.name = "iniciando_conexao"
		self.lcd.move_to(4, 1)
		self.lcd.putstr("Labs-AUTO-02")
		self.lcd.move_to(4, 2)
		self.lcd.putstr("Conectando...")
		# self.lcd.move_to(4, 3)
		# self.lcd.putstr("Outra")
		# self.lcd.move_to(3, 2)
		# self.lcd.putstr("~")

	@mestre
	def online(self):
		self.name = "online"
		self.lcd.move_to(3, 1)
		self.lcd.putstr("Opere pelo app")
		self.lcd.move_to(14, 3)
		self.lcd.putstr("Voltar")
		self.lcd.move_to(13, 3)
		self.lcd.overwrite("~")

	@mestre
	def erro_conexao(self):
		self.name = "erro_conexao"
		self.lcd.move_to(1, 0)
		self.lcd.putstr("Tentar novamente?")
		self.lcd.move_to(1, 2)
		self.lcd.putstr("~")
		self.lcd.putstr("Sim")
		self.lcd.move_to(15, 2)
		self.lcd.putstr("Nao")
		self.lcd.move_to(1, 2)

	@mestre
	def offline(self):
		self.name = "offline"
		self.lcd.move_to(1, 0)
		self.lcd.putstr("Escolha os ganhos:")
		self.lcd.move_to(0, 1)
		self.lcd.putstr("Kp: 00.00\n")
		self.lcd.move_to(0, 2)
		self.lcd.putstr("Ki: 00.00\n")
		self.lcd.move_to(0, 3)
		self.lcd.putstr("Kd: 00.00\n")
		self.lcd.move_to(13, 3)
		self.lcd.putstr("Voltar")
		self.lcd.move_to(4, 1)
		self.lcd.show_cursor()
		# self.lcd.cursor_y += 1
		# lcd.put
		# "Kp: 00.00 Ki: 00.00 Kd: 00.00"

	@mestre
	def setpoint(self):
		self.name = "setpoint"
		self.lcd.clear()
		self.lcd.hide_cursor()
		self.lcd.move_to(0, 0)
		self.lcd.putstr("Setpoint: 135")
		self.lcd.move_to(0, 3)
		self.lcd.putstr('Segure para retornar')
		self.lcd.move_to(10, 0)
		self.lcd.show_cursor()
